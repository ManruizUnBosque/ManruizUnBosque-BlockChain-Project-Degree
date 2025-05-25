from flask import Blueprint
from app.controllers.stream_controller import (
    list_streams_controller,
    publish_to_stream_controller,
    get_publications_controller,
    view_publication_controller,
    get_stream_history_controller # Importar el nuevo controlador
)

# Creamos un Blueprint. 'stream_api' es el nombre del blueprint.
# url_prefix añade '/api' al inicio de todas las rutas definidas en este blueprint.
stream_bp = Blueprint('stream_api', __name__, url_prefix='/api')

@stream_bp.route('/streams', methods=['GET'])
def get_streams_route():
    return list_streams_controller()

@stream_bp.route('/publish/<string:stream_name>', methods=['POST'])
def publish_to_stream_route(stream_name):
    return publish_to_stream_controller(stream_name)

@stream_bp.route('/publications/<string:stream_name>', methods=['GET'])
def get_publications_route(stream_name):
    return get_publications_controller(stream_name)

# --- Nueva Ruta para ver la publicación desde el QR ---
@stream_bp.route('/view_publication/<string:txid>', methods=['GET'])
def view_publication_route(txid):
    return view_publication_controller(txid)

# --- Nueva Ruta para ver el historial de un stream ---
@stream_bp.route('/stream/<string:stream_name>/history', methods=['GET'])
def get_stream_history_route(stream_name):
    return get_stream_history_controller(stream_name)

