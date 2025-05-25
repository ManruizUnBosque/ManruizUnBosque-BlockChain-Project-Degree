import os
import hashlib
from flask import request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from app.services.multichain_service import registrar_cambio_estado_documento # <--- AÑADIDO
from app.models.models import Documento
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Carpeta donde se guardarán los archivos subidos.
# 'static' es la carpeta que Flask sirve por defecto para archivos estáticos.
# 'uploads/proyectos_grado' es una subcarpeta dentro de 'static'.
UPLOAD_FOLDER = 'static/uploads/proyectos_grado'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'gif'} # Tipos de archivo permitidos

def allowed_file(filename):
    """Verifica si la extensión del archivo está permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_controller():
    """
    Controlador para subir archivos.
    Guarda el archivo en el servidor y devuelve su nombre, ruta y hash.
    También registra el evento de creación en la trazabilidad de MultiChain.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) # Asegura el nombre del archivo
        
        # Construir la ruta completa para guardar el archivo
        # current_app.root_path es la ruta raíz de tu aplicación Flask
        # UPLOAD_FOLDER se define relativo a la carpeta 'static' que está al mismo nivel que 'app'
        # Por lo tanto, necesitamos construir la ruta desde la raíz de la aplicación.
        # Si 'static' está en la raíz del proyecto:
        # upload_path_dir = os.path.join(current_app.root_path, '..', UPLOAD_FOLDER) # Si UPLOAD_FOLDER es 'static/uploads'
        # Si UPLOAD_FOLDER ya incluye 'static', y 'static' está en la raíz:
        # upload_path_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'proyectos_grado')
        # La forma más robusta es usar current_app.static_folder si UPLOAD_FOLDER es relativo a static
        
        # Asumiendo que UPLOAD_FOLDER = 'static/uploads/proyectos_grado'
        # y que 'static' está en la raíz del proyecto (al mismo nivel que 'run.py')
        # current_app.root_path apunta a la carpeta 'app'
        # Para llegar a 'static' desde 'app', subimos un nivel y luego entramos a 'static'
        
        # Corrección: Si UPLOAD_FOLDER es 'static/uploads/proyectos_grado',
        # y 'static' es la carpeta estática configurada en Flask (generalmente en la raíz del proyecto),
        # la ruta se construye mejor así:
        relative_upload_folder = os.path.join('uploads', 'proyectos_grado') # Parte de la ruta dentro de 'static'
        upload_dir_absolute = os.path.join(current_app.static_folder, relative_upload_folder)

        if not os.path.exists(upload_dir_absolute):
            os.makedirs(upload_dir_absolute)
            
        filepath_absolute = os.path.join(upload_dir_absolute, filename)
        
        try:
            file.save(filepath_absolute)
            
            # Calcular el hash SHA-256 del archivo
            sha256_hash = hashlib.sha256()
            with open(filepath_absolute, "rb") as f:
                # Leer y actualizar el hash en bloques para no cargar archivos grandes en memoria
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            file_hash = sha256_hash.hexdigest()
            
            # Generar la URL pública para acceder al archivo
            file_url = url_for('static', filename=os.path.join(relative_upload_folder, filename), _external=True)

            # --- INICIO: Registrar evento de creación en MultiChain ---
            current_app.logger.info(f"Registrando evento de creación para documento_id: {file_hash} (archivo: {filename})")
            respuesta_multichain = registrar_cambio_estado_documento(
                documento_id=file_hash,
                nuevo_estado="CREACION_REGISTRO", # Estado inicial para la trazabilidad
                usuario_id="sistema_carga", # Identificador del proceso/usuario que carga. Ajustar según sea necesario.
                detalles_adicionales={
                    "filename_original": filename,
                    "mensaje": "Documento cargado inicialmente al sistema."
                }
            )

            txid_trazabilidad = None
            if respuesta_multichain and respuesta_multichain.get("result"):
                txid_trazabilidad = respuesta_multichain.get("result")
                current_app.logger.info(f"Evento de creación registrado en MultiChain para {file_hash}. TXID: {txid_trazabilidad}")
            elif respuesta_multichain and respuesta_multichain.get("error"):
                # Loguear el error pero continuar, ya que el archivo se subió.
                # Podrías decidir manejar esto de forma diferente (ej. borrar el archivo si la trazabilidad es crítica).
                current_app.logger.error(f"Error al registrar evento de creación en MultiChain para {file_hash}: {respuesta_multichain['error'].get('message', 'Error desconocido')}")
            else:
                current_app.logger.error(f"Respuesta inesperada de registrar_cambio_estado_documento para {file_hash}: {respuesta_multichain}")
            # --- FIN: Registrar evento de creación en MultiChain ---
            
            # Guardar en la base de datos
            nuevo_documento = Documento(
                nombre=filename,
                ruta=file_url,  # o filepath_absolute si prefieres la ruta local
                hash_sha256=file_hash,
                user_id=2  # <-- Siempre asigna 2 como user_id
            )
            db.session.add(nuevo_documento)
            db.session.commit()
            return jsonify({
                "message": "File uploaded successfully and traceability event initiated",
                "filename": filename,
                "filepath_url": file_url, 
                "file_hash_sha256": file_hash,
                "trazabilidad_txid": txid_trazabilidad # Puede ser None si el registro en MultiChain falló
            }), 201
            
        except Exception as e:
            current_app.logger.error(f"Error saving file or calculating hash: {str(e)}")
            return jsonify({"error": f"Could not save file or calculate hash: {str(e)}"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

# Necesitarás registrar este controlador en un Blueprint y luego en la app,
# similar a como hiciste con stream_routes.

# Ejemplo de cómo registrarías esto (en un nuevo archivo app/routes/file_routes.py):
"""
from flask import Blueprint
from app.controllers.file_controller import upload_file_controller

file_bp = Blueprint('file_api', __name__, url_prefix='/api')

@file_bp.route('/upload_document', methods=['POST'])
def upload_document_route():
    return upload_file_controller()
"""

# Y luego en app/__init__.py:
"""
# ... otras importaciones ...
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes.stream_routes import stream_bp
    app.register_blueprint(stream_bp)

    from app.routes.file_routes import file_bp # IMPORTAR NUEVO BLUEPRINT
    app.register_blueprint(file_bp) # REGISTRAR NUEVO BLUEPRINT

    with app.app_context():
        db.create_all()

    return app
"""


@jwt_required()
def listar_mis_proyectos_controller():
    """
    Returns the list of projects (documents) for the authenticated user.
    """
    user_id = get_jwt_identity()
    try:
        mis_documentos = Documento.query.filter_by(user_id=user_id).all()
        proyectos = []
        for doc in mis_documentos:
            proyectos.append({
                "id": doc.id,
                "nombre": doc.nombre,
                "ruta": doc.ruta,
                "hash_sha256": doc.hash_sha256
            })
        return jsonify({"proyectos": proyectos}), 200
    except Exception as e:
        current_app.logger.error(f"Error listing projects for user {user_id}: {str(e)}")
        return jsonify({"error": "Could not retrieve projects"}), 500