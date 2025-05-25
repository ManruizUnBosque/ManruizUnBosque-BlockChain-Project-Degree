from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app import db # Importar la instancia de SQLAlchemy
from app.models import Documento # Asumiendo que Documento está en app.models o app.models.models
from app.services.multichain_service import registrar_cambio_estado_documento # Importar el servicio

# Roles permitidos para aprobar documentos
ROLES_APROBACION = ['director_gestor', 'vicerrectoria', 'comite'] # Ajusta según tus necesidades

@jwt_required()
def aprobar_documento_controller(documento_hash): # Cambiamos doc_id por documento_hash
    claims = get_jwt()
    user_role = claims.get("role")
    user_id_actor = get_jwt_identity() # ID del usuario que realiza la acción (desde el token)

    if user_role not in ROLES_APROBACION:
        current_app.logger.warning(f"Usuario {user_id_actor} con rol {user_role} intentó aprobar documento {documento_hash} sin permiso.")
        return jsonify({"status": "error", "message": "No tienes permiso para aprobar documentos."}), 403

    documento = Documento.query.filter_by(hash_sha256=documento_hash).first()

    if not documento:
        current_app.logger.info(f"Intento de aprobar documento no encontrado con hash: {documento_hash}")
        return jsonify({"status": "error", "message": "Documento no encontrado."}), 404

    # Aquí defines el nuevo estado. Podrías pasarlo como parámetro o tener lógicas más complejas.
    # Por simplicidad, asumiremos un estado genérico "APROBADO_POR_ROL"
    nuevo_estado = f"APROBADO_POR_{user_role.upper()}"
    
    # Comentario para la trazabilidad
    comentario_trazabilidad = f"Documento aprobado por {user_role} (ID: {user_id_actor})."

    try:
        # 1. Actualizar estado en la base de datos local
        documento.estado = nuevo_estado # Asegúrate que tu modelo Documento tiene un campo 'estado'
        db.session.commit()
        current_app.logger.info(f"Documento {documento_hash} actualizado a estado '{nuevo_estado}' en BD por usuario {user_id_actor}.")

        # 2. Registrar el evento en MultiChain
        # El actor_id para MultiChain podría ser el user_id_actor o un identificador más genérico del rol/sistema
        trazabilidad_txid = registrar_cambio_estado_documento(
            documento_hash=documento_hash,
            nuevo_estado=nuevo_estado,
            actor_id=str(user_id_actor), # Convertir a string si es necesario para MultiChain
            detalles_adicionales={"comentario": comentario_trazabilidad, "rol_aprobador": user_role}
        )
        current_app.logger.info(f"Evento de aprobación para documento {documento_hash} registrado en MultiChain. TXID: {trazabilidad_txid}")

        return jsonify({
            "status": "success",
            "message": f"Documento {documento_hash} aprobado exitosamente por {user_role}. Nuevo estado: {nuevo_estado}.",
            "trazabilidad_txid": trazabilidad_txid
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al aprobar documento {documento_hash}: {e}")
        return jsonify({"status": "error", "message": "Error interno al procesar la aprobación."}), 500

# Podrías añadir más controladores aquí, por ejemplo, para rechazar, solicitar revisión, etc.