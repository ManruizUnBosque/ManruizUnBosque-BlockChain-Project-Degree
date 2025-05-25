from flask import Blueprint
from app.controllers.document_controller import aprobar_documento_controller

document_bp = Blueprint('document_api', __name__, url_prefix='/api/documentos')

# Ruta para aprobar un documento, usando su hash como identificador
document_bp.add_url_rule('/<string:documento_hash>/aprobar', 
                         'aprobar_documento_route', 
                         aprobar_documento_controller, 
                         methods=['POST'])

# Aquí podrías añadir más rutas relacionadas con documentos:
# ej. /<string:documento_hash>/rechazar
# ej. /<string:documento_hash>/solicitar_revision