from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager # Ya no se necesita para JWT
from flask_jwt_extended import JWTManager # Importar JWTManager
from flask_cors import CORS
# Se você estiver usando Flask-Migrate, descomente:
# from flask_migrate import Migrate

db = SQLAlchemy()
# login_manager = LoginManager() # Ya no se necesita
# login_manager.login_view = 'auth_api.login_user_route'
# login_manager.login_message_category = 'info'
# login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."

jwt = JWTManager() # Crear instancia de JWTManager

# Se você estiver usando Flask-Migrate, descomente:
# migrate = Migrate()

# Ensure the following line is REMOVED or COMMENTED OUT if it exists:
# from .models import db # This line would cause issues

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Allow CORS for the frontend at localhost:5173
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.stream_routes import stream_bp
    app.register_blueprint(stream_bp)

    from app.routes.trazabilidad_routes import trazabilidad_bp
    app.register_blueprint(trazabilidad_bp)

    from app.routes.file_routes import file_bp
    app.register_blueprint(file_bp)
    
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.document_routes import document_bp
    app.register_blueprint(document_bp)

    from app.routes.student_dashboard_routes import student_dashboard_bp
    app.register_blueprint(student_dashboard_bp)

    return app
# Elimina la siguiente línea, es incorrecta y puede causar problemas:
# from app.models.models import Documento