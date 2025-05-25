from flask import jsonify, request
from app.models import db, StreamPublication
from app.services.multichain_service import call_multichain_rpc
import qrcode # Importar qrcode
import os # Importar os

def list_streams_controller():
    try:
        rpc_response = call_multichain_rpc("liststreams")
        if rpc_response.get('error'):
            return jsonify({"error": rpc_response['error']['message']}), 500
        streams = rpc_response.get('result', [])
        return jsonify({"streams": streams}), 200
    except Exception as e:
        # Loggear el error e
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

from flask import jsonify, request, current_app, url_for # Añadir current_app, url_for
from app.models import db, StreamPublication
from app.services.multichain_service import call_multichain_rpc
import qrcode # Importar qrcode
import os # Importar os
import binascii # Para decodificar hexadecimal

def list_streams_controller():
    try:
        rpc_response = call_multichain_rpc("liststreams")
        if rpc_response.get('error'):
            return jsonify({"error": rpc_response['error']['message']}), 500
        streams = rpc_response.get('result', [])
        return jsonify({"streams": streams}), 200
    except Exception as e:
        # Loggear el error e
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

def publish_to_stream_controller(stream_name):
    try:
        json_data = request.json
        if not json_data or 'data' not in json_data:
            return jsonify({"error": "No data provided"}), 400
        
        content_data = json_data['data']
        data_hex = content_data.encode('utf-8').hex()
        
        rpc_response = call_multichain_rpc("publish", [stream_name, "key1", data_hex])
        if rpc_response.get('error') and rpc_response['error'] is not None:
            return jsonify({"error": rpc_response['error']['message']}), 500
        
        txid = rpc_response.get('result')
        if not txid:
             return jsonify({"error": "No se pudo obtener txid de la publicación en MultiChain"}), 500

        publication = StreamPublication(stream_name=stream_name, data=content_data, txid=txid)
        
        # --- Inicio de la Lógica de Generación de QR ---
        # Crear el directorio para los QR si no existe
        # current_app.static_folder es usualmente 'static' en la raíz del proyecto
        qr_dir = os.path.join(current_app.static_folder, 'qrcodes')
        if not os.path.exists(qr_dir):
            os.makedirs(qr_dir)

        # URL que contendrá el QR (apuntará a un nuevo endpoint que crearemos)
        # Usamos url_for para construir la URL de forma segura
        # 'stream_api.view_publication_route' es el nombre del endpoint (Blueprint_name.function_name)
        qr_data_url = url_for('stream_api.view_publication_route', txid=txid, _external=True)
        
        qr_filename = f"{txid}.png"
        qr_filepath = os.path.join(qr_dir, qr_filename)
        
        # Generar y guardar la imagen QR
        img = qrcode.make(qr_data_url)
        img.save(qr_filepath)
        
        # Guardar la URL pública del QR en la base de datos
        # Esto asume que tienes una carpeta 'static' servida por Flask
        publication.qr_code_url = url_for('static', filename=f'qrcodes/{qr_filename}', _external=True)
        # --- Fin de la Lógica de Generación de QR ---

        db.session.add(publication)
        db.session.commit()
        
        return jsonify({
            "message": "Published successfully", 
            "txid": txid,
            "qr_code_url": publication.qr_code_url # Devolver la URL del QR
        }), 201
    except Exception as e:
        db.session.rollback() 
        current_app.logger.error(f"Error en publish_to_stream_controller: {str(e)}") # Mejor logging
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

def get_publications_controller(stream_name):
    try:
        publications = StreamPublication.query.filter_by(stream_name=stream_name).all()
        return jsonify({
            "stream_name": stream_name,
            "publications": [{"data": pub.data, "txid": pub.txid} for pub in publications]
        }), 200
    except Exception as e:
        # Loggear el error e
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# --- Nuevo Controlador para ver detalles de la publicación ---
def view_publication_controller(txid):
    try:
        publication = StreamPublication.query.filter_by(txid=txid).first()
        if not publication:
            return jsonify({"error": "Publicación no encontrada"}), 404

        # Opcional: Obtener datos frescos de MultiChain si es necesario
        # multichain_data = call_multichain_rpc("getstreamitem", [publication.stream_name, txid])
        # if multichain_data.get('error'):
        #     # Manejar error o simplemente mostrar datos de la DB
        #     pass

        response_data = {
            "id": publication.id,
            "stream_name": publication.stream_name,
            "data_db": publication.data, # Datos como están en la DB
            "txid": publication.txid,
            "qr_code_url": publication.qr_code_url,
            # "multichain_raw_data": multichain_data.get('result') # Si se consulta MultiChain
        }
        # Por ahora devolvemos JSON. Idealmente, aquí renderizarías una plantilla HTML.
        return jsonify(response_data), 200
    except Exception as e:
        current_app.logger.error(f"Error en view_publication_controller: {str(e)}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

def get_stream_history_controller(stream_name):
    try:
        # Llama a liststreamitems. Puedes ajustar los parámetros count, start, verbose según necesites.
        # verbose=True da más detalles, incluyendo 'data' (hex) y 'txid'.
        # count=-1 podría intentar traer todos, pero es mejor paginar para streams grandes.
        # Por defecto, trae los últimos 10.
        rpc_response = call_multichain_rpc("liststreamitems", [stream_name, True, 100, -100]) # Trae hasta 100 de los más recientes

        if rpc_response.get('error') and rpc_response['error'] is not None:
            return jsonify({"error": rpc_response['error']['message']}), 500
        
        items = rpc_response.get('result', [])
        
        processed_items = []
        for item in items:
            processed_item = {
                "txid": item.get("txid"),
                "publishers": item.get("publishers"),
                "keys": item.get("keys"),
                "confirmations": item.get("confirmations"),
                "blocktime": item.get("blocktime"),
                # Los datos suelen estar en hexadecimal en el campo 'data'
            }
            if 'data' in item and item['data']:
                try:
                    # Decodificar los datos de hexadecimal a texto (UTF-8)
                    processed_item['decoded_data'] = bytes.fromhex(item['data']).decode('utf-8')
                except (ValueError, UnicodeDecodeError) as e:
                    # Si no se puede decodificar (ej. no es texto o no es UTF-8)
                    processed_item['decoded_data'] = None
                    processed_item['raw_data_hex'] = item['data'] # Mantener el hexadecimal original
                    current_app.logger.warning(f"No se pudo decodificar data para txid {item.get('txid')}: {str(e)}")
            
            processed_items.append(processed_item)
            
        return jsonify({
            "stream_name": stream_name,
            "history": processed_items
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error en get_stream_history_controller: {str(e)}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# ... (otros imports)
from flask import jsonify, request, current_app # Asegúrate de que current_app esté importado
from app.services.multichain_service import call_multichain_rpc, registrar_nuevo_documento_en_trazabilidad # <<< AÑADIDO
import json
import hashlib

def publish_to_stream_controller():
    # ... existing code ...
    # Asumo que aquí tienes la lógica para obtener 'stream_name', 'key', y 'data_hex'
    # para publicar en el stream 'trabajos'.
    # Por ejemplo:
    # stream_name = "trabajos"
    # key = metadata_obj.get("file_hash_sha256") # o la clave que uses para 'trabajos'
    # data_hex = json.dumps(metadata_obj).encode('utf-8').hex()

    # Publicación en el stream principal 'trabajos'
    # response_trabajos = call_multichain_rpc("publish", [stream_name, key, data_hex])
    # if response_trabajos.get("error"):
    #     return jsonify({"status": "error", "message": f"Error al publicar en stream 'trabajos': {response_trabajos['error']['message']}"}), 500
    # txid_principal = response_trabajos.get("result")
    # current_app.logger.info(f"Documento {key} publicado en stream 'trabajos'. TXID: {txid_principal}")

    # <<< INICIO DE NUEVO CÓDIGO PARA TRAZABILIDAD >>>
    # Después de publicar exitosamente en el stream 'trabajos'
    # Necesitas obtener/definir:
    # 1. documento_id_trazabilidad: El ID único que usarás como clave en el stream 'trazabilidad_documentos'.
    #    Podría ser el mismo 'key' usado para el stream 'trabajos', como el hash SHA256 del archivo.
    # 2. usuario_id_actual: El ID del usuario que realiza la acción. Debes obtenerlo de tu sistema de autenticación.
    # 3. titulo_doc: Un título o nombre para el documento.
    # 4. hash_contenido_doc: El hash del contenido del documento.

    # Ejemplo (DEBES AJUSTAR ESTO A TUS VARIABLES REALES):
    # Supongamos que 'metadata_obj' contiene la información del archivo subido
    # y 'key' es el hash del archivo.
    if 'metadata_obj' in locals() and metadata_obj.get("file_hash_sha256"): # Verifica que metadata_obj exista y tenga el hash
        documento_id_trazabilidad = metadata_obj.get("file_hash_sha256")
        # Debes implementar la lógica para obtener el usuario_id_actual
        usuario_id_actual = "usuario_ejemplo" # REEMPLAZAR: Obtener de la sesión o token
        titulo_doc = metadata_obj.get("filename", "Sin título") # Usar filename o un campo de título
        hash_contenido_doc = metadata_obj.get("file_hash_sha256") # Asumiendo que es el mismo

        current_app.logger.info(f"Registrando trazabilidad inicial para documento: {documento_id_trazabilidad}")
        trazabilidad_response = registrar_nuevo_documento_en_trazabilidad(
            documento_id=documento_id_trazabilidad,
            usuario_id=usuario_id_actual,
            titulo_original=titulo_doc,
            hash_contenido=hash_contenido_doc
        )

        if trazabilidad_response.get("error"):
            current_app.logger.error(f"Error al registrar trazabilidad inicial para {documento_id_trazabilidad}: {trazabilidad_response['error'].get('message', 'Error desconocido')}")
            # Podrías decidir si este error debe detener el proceso o solo loggearse
        else:
            txid_trazabilidad = trazabilidad_response.get("result")
            current_app.logger.info(f"Trazabilidad inicial registrada para {documento_id_trazabilidad}. TXID: {txid_trazabilidad}")
    else:
        current_app.logger.warning("No se pudo registrar la trazabilidad inicial: 'metadata_obj' o 'file_hash_sha256' no encontrados.")
    # <<< FIN DE NUEVO CÓDIGO PARA TRAZABILIDAD >>>

    # ... el resto de tu función, por ejemplo, devolver la respuesta de la publicación en 'trabajos'
    # return jsonify({"status": "success", "message": "Publicado en stream 'trabajos' y trazabilidad registrada", "txid_trabajos": txid_principal, "txid_trazabilidad": txid_trazabilidad if 'txid_trazabilidad' in locals() else None}), 200
    # ... existing code ...