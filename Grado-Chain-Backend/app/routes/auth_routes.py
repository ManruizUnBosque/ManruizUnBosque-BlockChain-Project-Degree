from flask import Blueprint
from app.controllers.auth_controller import (
    register_user_controller, 
    login_user_controller, 
    logout_user_controller,
    protected_example_controller,
    refresh_token_controller # Importar el nuevo controlador
)
# from flask_login import login_required # Ya no se usa
from flask_jwt_extended import jwt_required # Importar jwt_required

auth_bp = Blueprint('auth_api', __name__, url_prefix='/api/auth')

auth_bp.add_url_rule('/register', 'register_user_route', register_user_controller, methods=['POST'])
auth_bp.add_url_rule('/login', 'login_user_route', login_user_controller, methods=['POST'])

# La ruta de logout ahora es más un indicativo para el cliente.
# Para un logout real del lado del servidor con denylist, se requeriría @jwt_required
auth_bp.add_url_rule('/logout', 'logout_user_route', logout_user_controller, methods=['POST']) 

# Ruta para refrescar el access token usando un refresh token
# El refresh token debe enviarse en el header Authorization: Bearer <refresh_token>
auth_bp.add_url_rule('/refresh', 'refresh_token_route', jwt_required(refresh=True)(refresh_token_controller), methods=['POST'])

# Ruta de ejemplo protegida
auth_bp.add_url_rule('/protected_example', 'protected_example_route', jwt_required()(protected_example_controller), methods=['GET'])