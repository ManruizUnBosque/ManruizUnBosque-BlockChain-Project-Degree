from flask import jsonify, current_app, request # Ensure 'request' is imported here
from app.services.multichain_service import obtener_eventos_trazabilidad_por_clave, registrar_cambio_estado_documento

def get_historial_documento_controller(documento_id):
    """
    Controlador para obtener el historial de trazabilidad de un documento específico.
    """
    stream_name = "trazabilidad_documentos" # El stream donde se guardan los eventos
    
    current_app.logger.info(f"Consultando historial de trazabilidad para documento_id: {documento_id} en stream: {stream_name}")
    
    # Ajusta count y start según necesites para paginación o para obtener todos los eventos
    # count=0 podría traer todos, pero es mejor paginar si son muchos. Usamos 100 por defecto.
    historial = obtener_eventos_trazabilidad_por_clave(stream_name, documento_id, verbose=True, count=100, start=-100)
    
    if historial is None:
        # Esto indica un error en la llamada RPC o al procesar la respuesta en el servicio
        current_app.logger.error(f"Error al obtener historial para documento_id: {documento_id}. El servicio devolvió None.")
        return jsonify({"status": "error", "message": "No se pudo obtener el historial del documento o ocurrió un error interno."}), 500
    
    if not historial: # Lista vacía
        current_app.logger.info(f"No se encontraron eventos de trazabilidad para documento_id: {documento_id}")
        return jsonify({
            "status": "success",
            "message": "No hay eventos de trazabilidad para este documento.",
            "documento_id": documento_id,
            "historial": []
        }), 200 # O 404 si prefieres indicar "no encontrado"

    current_app.logger.info(f"Historial encontrado para documento_id: {documento_id}. Número de eventos: {len(historial)}")
    return jsonify({
        "status": "success",
        "documento_id": documento_id,
        "historial": historial
    }), 200


def registrar_evento_documento_controller(documento_id):
    """
    Controlador para registrar un nuevo evento/cambio de estado para un documento existente.
    """
    data = request.get_json() # Now 'request' should be defined
    if not data:
        return jsonify({"status": "error", "message": "Cuerpo de la solicitud JSON vacío o inválido."}), 400

    nuevo_estado = data.get("nuevo_estado")
    usuario_id = data.get("usuario_id") # Idealmente, esto vendría de la sesión/token de autenticación
    detalles_adicionales = data.get("detalles_adicionales", {})

    if not nuevo_estado or not usuario_id:
        return jsonify({"status": "error", "message": "Los campos 'nuevo_estado' y 'usuario_id' son requeridos."}), 400

    current_app.logger.info(f"Registrando nuevo evento para documento_id: {documento_id}. Nuevo estado: {nuevo_estado}, Usuario: {usuario_id}")

    stream_name = "trazabilidad_documentos" # El stream donde se guardan los eventos
    
    # Llamamos a la función del servicio para registrar el cambio de estado
    respuesta_multichain = registrar_cambio_estado_documento(
        documento_id=documento_id,
        nuevo_estado=nuevo_estado,
        usuario_id=usuario_id,
        detalles_adicionales=detalles_adicionales
    )

    if respuesta_multichain.get("error"):
        current_app.logger.error(f"Error al registrar evento para documento_id {documento_id}: {respuesta_multichain['error'].get('message', 'Error desconocido')}")
        return jsonify({
            "status": "error",
            "message": f"Error al registrar el evento en MultiChain: {respuesta_multichain['error'].get('message', 'Error desconocido')}"
        }), 500

    txid_evento = respuesta_multichain.get("result")
    current_app.logger.info(f"Evento registrado exitosamente para documento_id {documento_id}. TXID: {txid_evento}")
    
    return jsonify({
        "status": "success",
        "message": "Evento registrado exitosamente en la trazabilidad.",
        "documento_id": documento_id,
        "nuevo_estado": nuevo_estado,
        "txid": txid_evento
    }), 201 # 201 Created, ya que se creó un nuevo recurso (el evento)