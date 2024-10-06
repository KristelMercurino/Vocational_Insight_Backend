from api.middleware.reset_pass import auth_middleware
from flask import Blueprint, jsonify, request, abort
from api import db
from api.models import Usuario
import bcrypt
import jwt  # Importamos jwt para generar el token
from datetime import datetime, timedelta
from dotenv import load_dotenv
from api.controllers.email import send_mail, pull_html_body
import os


# Cargar variables de entorno
load_dotenv()

# Definimos un blueprint para las rutas relacionadas con usuarios
reset_pass_bp = Blueprint('reset_pass_bp', __name__)

@reset_pass_bp.route('/restablecer_contrasenna', methods=['POST'])
def restablecer_contraseña():
    data = request.get_json()

    # Validar si el email está presente
    if 'email' not in data:
        abort(400, description="Falta el email")

    # Buscar el usuario por email
    usuario = Usuario.query.filter_by(email=data['email']).first()

    if usuario:
        # Generar el token JWT que expira en 30 minutos
        token = jwt.encode({
            'email': usuario.email,  # Guardamos el email en el payload
            'exp': datetime.utcnow() + timedelta(minutes=5)  # El token expirará en 30 minutos
        }, os.environ.get('RESTABLISH_SECRET_KEY'), algorithm='HS256')  # Cargar la clave desde el .env

        # Generar el cuerpo HTML del correo
        html_body = pull_html_body(token)

        # Enviar el correo
        send_mail(html_body, usuario.email)

        return jsonify({"message": "Se ha enviado un correo para restablecer la contraseña."}), 200
    else:
        abort(404, description="Usuario no encontrado")


@reset_pass_bp.route('/restablecer_contrasenna_confirmar', methods=['POST'])
def restablecer_contraseña_confirmar():
    # Extraer el token del encabezado 'Authorization'
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]  # Extraemos el token JWT

    if not token:
        abort(400, description="Token faltante")

    data = request.get_json()

    # Validar si la nueva contraseña está presente
    if 'new_password' not in data:
        abort(400, description="Falta la nueva contraseña")

    new_password = data['new_password']

    try:
        # Verificar y decodificar el token
        payload = jwt.decode(token, os.environ.get('RESTABLISH_SECRET_KEY'), algorithms=['HS256'])
        
        # Obtener el email del payload
        email = payload['email']

        # Buscar al usuario por email
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            # Actualizar la contraseña
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            usuario.contrasena = hashed_password
            usuario.ultima_actualizacion = datetime.now()
            
            # Guardar los cambios en la base de datos
            db.session.commit()

            return jsonify({"message": "Contraseña restablecida correctamente."}), 200
        else:
            abort(404, description="Usuario no encontrado")

    except jwt.ExpiredSignatureError:
        abort(400, description="El token ha expirado")
    except jwt.InvalidTokenError:
        abort(400, description="Token inválido")
    except Exception as e:
        abort(500, description=str(e))  # Manejo de cualquier otro error