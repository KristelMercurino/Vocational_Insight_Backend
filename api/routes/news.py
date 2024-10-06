from flask import Blueprint, jsonify
from api.models import Noticias
from api.middleware.auth import auth_middleware

news_bp = Blueprint('news_bp', __name__)

# Servicio de noticias
@news_bp.route('/noticias', methods=['GET'])
@auth_middleware
def obtener_noticias(payload):
    # Consulta para obtener las 10 noticias más recientes, ordenadas por fecha de publicación descendente
    noticias = Noticias.query.order_by(Noticias.fecha_publicacion.desc()).limit(10).all()
    
    # Devolver las noticias en formato JSON
    return jsonify(noticias), 200


