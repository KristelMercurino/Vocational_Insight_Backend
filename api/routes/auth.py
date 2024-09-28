from flask import Blueprint, jsonify, request, abort
from api import db
from api.models import Usuario
import bcrypt  # Para manejar el hash de contraseñas
import jwt  # Para manejar JWT
from datetime import datetime, timedelta

# Clave secreta para firmar los tokens JWT (manténla segura y confidencial)
SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsJ9.eyJpZF91c3VhcmjE3MjYwNzYzNjN9.Wk8cezbc2Sf'

# Definimos un blueprint para las rutas relacionadas con la autenticación
auth_bp = Blueprint('auth_bp', __name__)

# Ruta para el inicio de sesión (Login - POST)
@auth_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    
    # Validar si los datos requeridos están presentes
    if not all(key in datos for key in ('email', 'contrasena')):
        abort(400, description="Faltan datos requeridos")

    # Buscar el usuario por email
    usuario = Usuario.query.filter_by(email=datos['email']).first()

    if usuario:
        # Verificar la contraseña proporcionada con la contraseña encriptada en la base de datos
        if bcrypt.checkpw(datos['contrasena'].encode('utf-8'), usuario.contrasena.encode('utf-8')):
            
            # Generar el token JWT
            token = jwt.encode({
                'id_usuario': usuario.id_usuario,
                'exp': datetime.utcnow() + timedelta(hours=24)  # El token expirará en 24 horas
            }, SECRET_KEY, algorithm='HS256')

            # Devolver el token JWT
            return jsonify({
                'token': token,
                'message': 'Inicio de sesión exitoso'
            }), 200
        else:
            # Si la contraseña no coincide
            abort(401, description="Contraseña incorrecta")
    else:
        # Si no se encuentra un usuario con ese email
        abort(404, description="Usuario no encontrado")
