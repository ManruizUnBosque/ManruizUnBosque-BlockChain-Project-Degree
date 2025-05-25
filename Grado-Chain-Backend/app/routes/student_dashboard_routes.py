from flask import Blueprint
from app.controllers.student_dashboard_controller import student_dashboard_stats_controller

student_dashboard_bp = Blueprint('student_dashboard_api', __name__, url_prefix='/api/student')

student_dashboard_bp.add_url_rule('/dashboard', 'dashboard_stats', student_dashboard_stats_controller, methods=['GET'])