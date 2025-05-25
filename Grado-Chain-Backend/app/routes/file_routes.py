from flask import Blueprint
from app.controllers.file_controller import upload_file_controller, listar_mis_proyectos_controller

file_bp = Blueprint('file_api', __name__, url_prefix='/api')

@file_bp.route('/upload_document', methods=['POST'])
def upload_document_route():
    return upload_file_controller()

@file_bp.route('/mis_proyectos', methods=['GET'])
def listar_mis_proyectos_route():
    return listar_mis_proyectos_controller()