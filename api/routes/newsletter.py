from flask import Blueprint, jsonify, request, abort
from api import db
from datetime import datetime
from api.models import BoletinInformativo
from api.middleware.auth import auth_middleware

# Definimos un blueprint para las rutas relacionadas con boletines
newsletter_bp = Blueprint('newsletter_bp', __name__)

# Ruta para crear un nuevo boletín informativo (Create - POST)
@newsletter_bp.route('/agregar_boletines', methods=['POST'])
@auth_middleware
def nuevo_boletin(payload):
    datos = request.get_json()
    
    # Validar si los datos requeridos están presentes
    if not isinstance(datos, list) or not all(all(key in boletin for key in ('titulo', 'contenido', 'fuente', 'link_mas_informacion')) for boletin in datos):
        abort(400, description="Faltan datos requeridos")

    try:
        for boletin_datos in datos:
            # Crear un nuevo boletín con los datos recibidos, incluyendo el id_usuario
            nuevo_boletin = BoletinInformativo(
                titulo=boletin_datos['titulo'],
                contenido=boletin_datos['contenido'].replace("{nombre}", f"{payload['nombre']}"),  # Saludar al usuario logueado
                fuente=boletin_datos['fuente'],
                link_mas_informacion=boletin_datos['link_mas_informacion'],
                fecha_envio=datetime.utcnow(),  # Cambiado a fecha_envio
                id_usuario=payload['id_usuario']  # Usar el id del usuario logueado
            )

            # Agregar el nuevo boletín a la base de datos
            db.session.add(nuevo_boletin)

        db.session.commit()  # Confirmar los cambios en la base de datos

        return jsonify({'message': 'Boletines creados con éxito', 'total_boletines': len(datos)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para listar los boletines con paginación (Read - GET)
@newsletter_bp.route('/boletines', methods=['GET'])
@auth_middleware
def obtener_boletines():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    boletines_pag = BoletinInformativo.query.paginate(page=page, per_page=per_page)

    boletines = [
        {
            'id_boletin': boletin.id_boletin,
            'titulo': boletin.titulo,
            'contenido': boletin.contenido,
            'fuente': boletin.fuente,
            'link_mas_informacion': boletin.link_mas_informacion,
            'fecha_envio': boletin.fecha_envio.isoformat(),  # Cambiado a fecha_envio
            'usuario': f"{boletin.usuario.nombre} {boletin.usuario.apellido}" if boletin.usuario else "Usuario desconocido"
        }
        for boletin in boletines_pag.items
    ]

    return jsonify({
        'boletines': boletines,
        'pagina_actual': boletines_pag.page,
        'total_boletines': boletines_pag.total,
        'total_paginas': boletines_pag.pages
    }), 200
