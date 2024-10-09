from flask import Blueprint, request, jsonify
from api import db
from api.models import Usuario
from api.middleware.auth import auth_middleware

# Definir un blueprint para manejar las solicitudes de suscripción
suscription_bp = Blueprint('suscription_bp', __name__)

# Ruta para actualizar la suscripción del usuario
@suscription_bp.route('/suscripcion', methods=['POST'])
@auth_middleware  # Usar el middleware para obtener la autenticación del usuario
def suscribirme(payload):
    try:
        # Obtener el ID del usuario desde el payload del middleware
        id_usuario = payload['id_usuario']
        
        # Buscar al usuario por su ID en la base de datos
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()

        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Verificar el estado actual de la suscripción
        if usuario.suscripcion_boletin == 1:
            return jsonify({'message': 'Usuario ya está suscrito', 'estado_actual': usuario.suscripcion_boletin}), 200

        # Actualizar el campo suscripcion_boletin a 1 (suscribir al usuario)
        usuario.suscripcion_boletin = 1

        # Guardar los cambios en la base de datos
        db.session.commit()

        # Responder con un mensaje de éxito
        return jsonify({'message': 'Usuario suscrito con éxito', 'estado_actualizado': usuario.suscripcion_boletin}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
