from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Documento

@jwt_required()
def student_dashboard_stats_controller():
    user_id = get_jwt_identity()
    # Filtrar documentos por el usuario autenticado
    total = Documento.query.filter_by(user_id=user_id).count()
    en_revision = Documento.query.filter_by(user_id=user_id, estado="EN_REVISION").count()
    rechazados = Documento.query.filter_by(user_id=user_id, estado="RECHAZADO").count()

    return jsonify({
        "proyectos_totales": total,
        "en_revision": en_revision,
        "rechazados": rechazados
    }), 200
