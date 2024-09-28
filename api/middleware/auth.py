from functools import wraps
from flask import request, jsonify, abort
import jwt

SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsJ9.eyJpZF91c3VhcmjE3MjYwNzYzNjN9.Wk8cezbc2Sf'

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
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        # Pasamos el payload como argumento
        return f(payload, *args, **kwargs)

    return decorador


