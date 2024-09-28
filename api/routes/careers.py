from flask import Blueprint, jsonify, request, abort
from api import db
from api.models import Usuario
import jwt  # Para manejar JWT
from api.models import Carrera

careers_bp = Blueprint('careers_bp', __name__)

@careers_bp.route('/carreras', methods=['GET'])
def listar_carreras():
    try:
        # Obtener parámetros de paginación de la solicitud (si no se envían, usar valores por defecto)
        page = request.args.get('page', 1, type=int)  # Número de página, por defecto 1
        per_page = request.args.get('per_page', 10, type=int)  # Carreras por página, por defecto 10

        # Realizar la consulta con paginación
        carreras_paginated = Carrera.query.paginate(page=page, per_page=per_page, error_out=False)

        # Extraer las carreras de la página actual
        carreras_json = [
            {
                'id_carrera': carrera.id_carrera,
                'codigo_carrera': carrera.codigo_carrera,
                'nombre_carrera': carrera.nombre_carrera,
                'area_carrera': carrera.area_carrera,
                'subarea_carrera': carrera.subarea_carrera,
                'duracion_carrera': carrera.duracion_carrera,
                'nivel_global': carrera.nivel_global,
                'nivel_academico': carrera.nivel_academico,
                'nombre_instituto': carrera.nombre_instituto,
                'jornada': carrera.jornada,
                'modalidad': carrera.modalidad,
                'nombre_sede': carrera.nombre_sede,
                'sede_comuna': carrera.sede_comuna,
                'acreditacion': carrera.acreditacion,
                'salario_promedio': carrera.salario_promedio,
                'empleabilidad': carrera.empleabilidad
            }
            for carrera in carreras_paginated.items  # Solo las carreras de la página actual
        ]

        # Devolver la respuesta con los datos paginados
        return jsonify({
            'carreras': carreras_json,
            'page': carreras_paginated.page,  # Página actual
            'total_pages': carreras_paginated.pages,  # Total de páginas
            'total_carreras': carreras_paginated.total  # Total de carreras
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
