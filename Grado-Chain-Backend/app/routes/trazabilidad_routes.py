from flask import Blueprint
from app.controllers.trazabilidad_controller import get_historial_documento_controller, registrar_evento_documento_controller # Añadir registrar_evento_documento_controller

trazabilidad_bp = Blueprint('trazabilidad_api', __name__, url_prefix='/api/trazabilidad')

@trazabilidad_bp.route('/documento/<string:documento_id>', methods=['GET'])
def get_historial_documento_route(documento_id):
    """
    Ruta para obtener el historial de trazabilidad de un documento por su ID.
    El ID del documento es la clave usada en el stream 'trazabilidad_documentos'.
    """
    return get_historial_documento_controller(documento_id)

@trazabilidad_bp.route('/documento/<string:documento_id>/evento', methods=['POST'])
def registrar_evento_documento_route(documento_id):
    """
    Ruta para registrar un nuevo evento (cambio de estado, etc.) para un documento.
    Espera un cuerpo JSON con:
    {
        "nuevo_estado": "ESTADO_DEL_EVENTO",
        "usuario_id": "ID_DEL_USUARIO_ACTOR",
        "detalles_adicionales": { "clave_extra": "valor_extra", ... } // Opcional
    }
    """
    return registrar_evento_documento_controller(documento_id)