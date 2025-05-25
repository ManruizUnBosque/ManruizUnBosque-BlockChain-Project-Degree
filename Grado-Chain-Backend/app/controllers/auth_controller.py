from flask import request, jsonify, current_app
from app.models import db, User
# from flask_login import login_user, logout_user, current_user, login_required # Ya no se usan directamente para JWT
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

def register_user_controller():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Request body must be JSON"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'estudiante')

    # Normalizar el rol recibido para que coincida con los valores internos
    role_map = {
        'estudiante': 'estudiante',
        'docente': 'docente',
        'director_gestor': 'director_gestor',
        'vicerrectoria': 'vicerrectoria'
    }
    # Si el rol viene en formato frontend, lo convertimos
    role = role_map.get(role, role.lower())

    if role not in ['estudiante', 'docente', 'director_gestor', 'vicerrectoria']:
        return jsonify({"status": "error", "message": "Invalid role specified"}), 400

    if not username or not email or not password:
        return jsonify({"status": "error", "message": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"status": "error", "message": "Email already registered"}), 400

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"User {username} registered successfully with role {role}.")
        # No se hace login automático aquí con JWT, el cliente solicitará tokens por separado
        return jsonify({"status": "success", "message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error registering user {username}: {e}")
        return jsonify({"status": "error", "message": "Registration failed due to an internal error"}), 500

def login_user_controller():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Request body must be JSON"}), 400

    identifier = data.get('identifier') 
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"status": "error", "message": "Identifier (username or email) and password are required"}), 400

    user_by_username = User.query.filter_by(username=identifier).first()
    user_by_email = User.query.filter_by(email=identifier).first()
    
    user = user_by_username or user_by_email

    if user and user.check_password(password):
        # La identidad del token puede ser el ID del usuario o cualquier otro identificador único.
        # También podemos añadir claims adicionales si es necesario.
        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role, "username": user.username})
        refresh_token = create_refresh_token(identity=user.id) # El refresh token usualmente solo lleva la identidad
        
        current_app.logger.info(f"User {user.username} logged in successfully. Tokens created.")
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"username": user.username, "email": user.email, "role": user.role}
        }), 200
    
    current_app.logger.warning(f"Failed login attempt for identifier: {identifier}")
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

def refresh_token_controller():
    # Esta ruta requiere un refresh token válido en el header Authorization: Bearer <refresh_token>
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
         return jsonify({"status": "error", "message": "User not found for token refresh"}), 404
    
    # Se pueden añadir claims adicionales al nuevo access token si es necesario
    new_access_token = create_access_token(identity=current_user_id, additional_claims={"role": user.role, "username": user.username})
    current_app.logger.info(f"Access token refreshed for user ID: {current_user_id}")
    return jsonify({"status": "success", "access_token": new_access_token}), 200

# Logout con JWT es principalmente una operación del lado del cliente (borrar el token).
# Para un logout real del lado del servidor, se necesitaría una "denylist" (lista de tokens revocados).
# Esta es una implementación más avanzada. Por ahora, esta ruta es un placeholder.
def logout_user_controller():
    # Para un logout real con denylist, se añadiría el JTI (JWT ID) del token a una lista de revocados.
    # jti = get_jwt()['jti']
    # add_to_denylist(jti) # Esta función necesitaría ser implementada
    current_app.logger.info(f"Logout request received. Client should discard tokens.")
    return jsonify({"status": "success", "message": "Logout successful. Please discard your tokens."}), 200


def protected_example_controller():
    current_user_id = get_jwt_identity() # Obtiene la identidad del token (user.id en nuestro caso)
    # claims = get_jwt() # Obtiene todos los claims del token, incluyendo los adicionales
    # user_role = claims.get("role")
    # username = claims.get("username")
    
    # Opcionalmente, cargar el usuario desde la BD si necesitas más info que no esté en el token
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    return jsonify({
        "status": "success",
        "message": f"Hello, {user.username}! You are accessing a protected area.",
        "user_id": current_user_id,
        "role": user.role # O user_role si lo tomas directamente del claim
    }), 200