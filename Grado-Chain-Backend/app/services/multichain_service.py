import requests
from flask import current_app # Para acceder a app.config
import json
from datetime import datetime # <<< AÑADIDO: Importar datetime

def call_multichain_rpc(method, params=[]):
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    try:
        response = requests.post(
            f"http://{current_app.config['MULTICHAIN_RPC_HOST']}:{current_app.config['MULTICHAIN_RPC_PORT']}",
            auth=(current_app.config['MULTICHAIN_RPC_USER'], current_app.config['MULTICHAIN_RPC_PASSWORD']),
            json=payload,
            timeout=10 # Añadir un timeout es una buena práctica
        )
        response.raise_for_status() # Lanza una excepción para errores HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error en la llamada RPC a MultiChain: {e}")
        return {"error": {"message": f"Error de comunicación con MultiChain: {str(e)}"}, "result": None}
    except ValueError as e: # Si la respuesta no es JSON
        current_app.logger.error(f"Error al decodificar JSON de MultiChain: {e}. Respuesta recibida: {response.text if 'response' in locals() else 'No response object'}")
        return {"error": {"message": f"Respuesta inválida de MultiChain: {str(e)}"}, "result": None}

# --- Funciones de Trazabilidad ---

def registrar_evento_trazabilidad(stream_name, key, data_evento_obj):
    """
    Publica un evento de trazabilidad (objeto Python) en un stream de MultiChain.
    Convierte el objeto de datos a JSON y luego a hexadecimal.
    Args:
        stream_name (str): El nombre del stream.
        key (str): La clave para el ítem del stream (ej. ID del documento).
        data_evento_obj (dict): El objeto Python con los datos del evento.
    Returns:
        dict: La respuesta de la llamada RPC.
    """
    try:
        data_hex = json.dumps(data_evento_obj).encode('utf-8').hex()
        return call_multichain_rpc("publish", [stream_name, key, data_hex])
    except Exception as e:
        current_app.logger.error(f"Error al preparar datos para registrar evento de trazabilidad: {e}")
        return {"error": {"message": f"Error interno al registrar evento: {str(e)}"}, "result": None}

def registrar_nuevo_documento_en_trazabilidad(documento_id, usuario_id, titulo_original, hash_contenido):
    """Registra el evento de creación de un nuevo documento en el stream de trazabilidad."""
    stream_name = "trazabilidad_documentos" # Nombre del stream de trazabilidad
    evento_data = {
        "documento_id": documento_id, # Clave principal del evento
        "evento_tipo": "CREACION_REGISTRO",
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "actor_id": usuario_id,
        "detalles": {
            "titulo_original": titulo_original,
            "hash_contenido_inicial": hash_contenido
        }
    }
    return registrar_evento_trazabilidad(stream_name, documento_id, evento_data)

def registrar_cambio_estado_documento(documento_id, nuevo_estado, usuario_id, detalles_adicionales={}):
    """Registra un cambio de estado de un documento en el stream de trazabilidad."""
    stream_name = "trazabilidad_documentos"
    evento_data = {
        "documento_id": documento_id,
        "evento_tipo": "CAMBIO_ESTADO",
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "actor_id": usuario_id,
        "detalles": {
            "nuevo_estado": nuevo_estado,
            **detalles_adicionales # Para fusionar diccionarios si hay más detalles
        }
    }
    return registrar_evento_trazabilidad(stream_name, documento_id, evento_data)

def obtener_eventos_trazabilidad_por_clave(stream_name, key, verbose=True, count=100, start=-100):
    """
    Obtiene eventos de trazabilidad de un stream por clave (ej. todos los eventos de un documento_id).
    Args:
        stream_name (str): El nombre del stream.
        key (str): La clave a buscar (ej. ID del documento).
        verbose (bool): Si se devuelven los datos completos.
        count (int): Número máximo de ítems a devolver.
        start (int): Para paginación, ítem desde el cual empezar.
    Returns:
        list: Lista de eventos decodificados o None si hay error.
    """
    rpc_response = call_multichain_rpc("liststreamkeyitems", [stream_name, key, verbose, count, start])
    
    if rpc_response.get('error') and rpc_response['error'] is not None:
        current_app.logger.error(f"Error de MultiChain al obtener eventos por clave '{key}' en stream '{stream_name}': {rpc_response['error']['message']}")
        return None # O podrías devolver una lista vacía o propagar el error

    items_from_blockchain = rpc_response.get('result', [])
    processed_items = []
    for item in items_from_blockchain:
        if 'data' in item and item['data']:
            try:
                decoded_data_str = bytes.fromhex(item['data']).decode('utf-8')
                data_obj = json.loads(decoded_data_str)
                # Añadir información del bloque/transacción al evento si es útil
                processed_item = {
                    "txid": item.get("txid"),
                    "confirmations": item.get("confirmations"),
                    "blocktime": item.get("blocktime"),
                    "publishers": item.get("publishers"),
                    "key": item.get("keys")[0] if item.get("keys") else key, # La clave del ítem
                    "evento_registrado": data_obj # Los datos del evento que publicaste
                }
                processed_items.append(processed_item)
            except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as e:
                current_app.logger.warning(f"No se pudo decodificar data de blockchain para txid {item.get('txid')} en stream '{stream_name}': {str(e)}")
                # Podrías añadir el ítem con datos crudos si es necesario
    return processed_items

def obtener_todos_los_eventos_trazabilidad(stream_name, verbose=True, count=100, start=-100):
    """
    Obtiene todos los eventos de trazabilidad de un stream.
    Args:
        stream_name (str): El nombre del stream.
        verbose (bool): Si se devuelven los datos completos.
        count (int): Número máximo de ítems a devolver.
        start (int): Para paginación.
    Returns:
        list: Lista de eventos decodificados o None si hay error.
    """
    rpc_response = call_multichain_rpc("liststreamitems", [stream_name, verbose, count, start])

    if rpc_response.get('error') and rpc_response['error'] is not None:
        current_app.logger.error(f"Error de MultiChain al obtener todos los eventos del stream '{stream_name}': {rpc_response['error']['message']}")
        return None

    items_from_blockchain = rpc_response.get('result', [])
    processed_items = []
    # (La lógica de procesamiento es similar a obtener_eventos_trazabilidad_por_clave)
    for item in items_from_blockchain:
        if 'data' in item and item['data']:
            try:
                decoded_data_str = bytes.fromhex(item['data']).decode('utf-8')
                data_obj = json.loads(decoded_data_str)
                processed_item = {
                    "txid": item.get("txid"),
                    "confirmations": item.get("confirmations"),
                    "blocktime": item.get("blocktime"),
                    "publishers": item.get("publishers"),
                    "keys": item.get("keys"),
                    "evento_registrado": data_obj
                }
                processed_items.append(processed_item)
            except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as e:
                current_app.logger.warning(f"No se pudo decodificar data de blockchain para txid {item.get('txid')} en stream '{stream_name}': {str(e)}")
    return processed_items