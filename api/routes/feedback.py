from flask import Blueprint, jsonify, request, abort
from api import db
from datetime import datetime
from api.models import Feedback  # Importa el modelo correcto (Feedback)
from api.models import Usuario
from api.middleware.auth import auth_middleware

# Definimos un blueprint para las rutas relacionadas con feedback
feedback_bp = Blueprint('feedback_bp', __name__)

# Ruta para crear un nuevo feedback (Create - POST)
@feedback_bp.route('/feedback', methods=['POST'])
@auth_middleware
def nuevo_feedback(payload):
    datos = request.get_json()

    # Validar si los datos requeridos están presentes
    if not all(key in datos for key in ('puntuacion', 'comentario')):
        abort(400, description="Faltan datos requeridos")

    # Crear un nuevo feedback 
    nuevo_feedback = Feedback(
        puntuacion=datos['puntuacion'],
        comentario=datos['comentario'],
        fecha_feedback=datetime.now()  # Guardar la fecha de creación
    )

    # Agregar el nuevo feedback a la base de datos
    db.session.add(nuevo_feedback)
    db.session.commit()  # Confirmar los cambios en la base de datos

    # Retornar una respuesta exitosa con el ID del feedback recién creado
    return jsonify({'message': 'Feedback enviado con éxito', 'id_feedback': nuevo_feedback.id_feedback}), 201

# servicio de listar opiniones de los usuarios
@feedback_bp.route('/opiniones_usuarios', methods=['GET'])
@auth_middleware
def obtener_opiniones(payload):
    usuario = Usuario.query.get_or_404(payload["id_usuario"])  # Usuario autenticado

    try:
        opiniones = Feedback.query.all()

        for feedback in opiniones:
            print(f"Feedback: {feedback.id_feedback}, Usuario: {feedback.usuario}")  # Verifica si la relación existe

        return jsonify([
            {
                'puntuacion': feedback.puntuacion,
                'comentario': feedback.comentario,
                'Nombre': f"{usuario.nombre} {usuario.apellido}"
            } for feedback in opiniones
        ]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

