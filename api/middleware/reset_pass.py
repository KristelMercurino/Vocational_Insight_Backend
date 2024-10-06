from functools import wraps
from flask import request, jsonify, abort
import jwt
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave secreta desde el archivo .env
RESTABLISH_SECRET_KEY = os.environ.get('RESTABLISH_SECRET_KEY')  # Asegúrate de que esté definida en tu .env

def auth_middleware(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None
        
        # Verificamos si el token JWT está presente en el encabezado 'Authorization'
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Extraemos el token JWT

        if not token:
            return jsonify({'message': 'Token faltante'}), 401

        try:
            # Decodificamos el token y obtenemos el payload (email y id del usuario)
            payload = jwt.decode(token, RESTABLISH_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        # Pasamos el payload como argumento
        return f(payload, *args, **kwargs)

    return decorador
