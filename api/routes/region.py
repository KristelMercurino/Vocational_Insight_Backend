from api.middleware.auth import auth_middleware
from api.models import Ciudad, Region
from flask import Blueprint, jsonify, request, abort

# Definimos un blueprint para las rutas relacionadas con usuarios
region_bp = Blueprint('region_bp', __name__)
# Ruta para obtener las ciudades relacionadas con una región seleccionada (para el filtro de ciudades)


@region_bp.route('/regiones/<int:id_region>/ciudades', methods=['GET'])
@auth_middleware
def obtener_ciudades_por_region(payload,id_region):
    # Consulta para obtener todas las ciudades que pertenecen a la región proporcionada
    ciudades = Ciudad.query.filter_by(id_region=id_region).all()
    
    # Devolver las ciudades en formato JSON
    return jsonify([
        {
            'id_ciudad': ciudad.id_ciudad,
            'nombre_ciudad': ciudad.ciudad
        } for ciudad in ciudades
    ]), 200  # Código de estado 200 indica éxito


#servicio de regiones
@region_bp.route('/regiones', methods=['GET'])
@auth_middleware
def obtener_regiones(payload):
    # Consulta para obtener todas las ciudades que pertenecen a la región proporcionada
    regiones = Region.query.all()
    
    # Devolver las ciudades en formato JSON
    return jsonify([
        {
            'id_region': region.id_region,
            'nombre_region': region.region
        } for region in regiones
    ]), 200  
