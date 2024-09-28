from api.middleware.auth import auth_middleware
from flask import Blueprint, jsonify, request, abort
from api import db
from api.models import Usuario
import bcrypt  # Importamos bcrypt para manejar el hash de contraseñas
from datetime import datetime # Ruta para desactivar un usuario (Update - PUT)

# Definimos un blueprint para las rutas relacionadas con usuarios
usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios/datos', methods=['GET'])
@auth_middleware
def obtener_usuario(payload):
    # El 'payload' ya contiene la información del usuario autenticado
    usuario = Usuario.query.get_or_404(payload["id_usuario"])
    
    # Devolvemos los datos del usuario solicitado
    return jsonify({
        'id_usuario': usuario.id_usuario,
        'email': usuario.email,
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'genero': usuario.genero,
        'fecha_nac': usuario.fecha_nac.strftime('%Y-%m-%d') if usuario.fecha_nac else None,
        'id_ciudad': usuario.id_ciudad
    }), 200


# Ruta para crear un nuevo usuario (Create - POST)
@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    
    # Validar si los datos requeridos están presentes
    if not all(key in datos for key in ('email', 'nombre', 'apellido', 'contrasena')):
        abort(400, description="Faltan datos requeridos")

    # Encriptar la contraseña utilizando bcrypt
    hashed_password = bcrypt.hashpw(datos['contrasena'].encode('utf-8'), bcrypt.gensalt())

    # Crear un nuevo usuario con los datos proporcionados
    nuevo_usuario = Usuario(
        email=datos['email'],  # Guardar el email
        nombre=datos['nombre'],  # Guardar el nombre
        apellido=datos['apellido'],  # Guardar el apellido
        genero=datos.get('genero'),  # Guardar el género si se proporciona
        fecha_nac=datos.get('fecha_nac'),  # Guardar la fecha de nacimiento si se proporciona
        contrasena=hashed_password.decode('utf-8'),  # Convertir la contraseña encriptada de bytes a string y almacenarla
        id_ciudad=datos.get('id_ciudad'),  # Relacionar el usuario con la ciudad seleccionada
        activo=1,  # El usuario está activo por defecto
        creacion_usuario = datetime.now()
    )

    # Agregar el nuevo usuario a la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()  # Confirmar los cambios en la base de datos

    # Retornar una respuesta exitosa con el ID del usuario recién creado
    return jsonify({'message': 'Usuario creado con éxito', 'id_usuario': nuevo_usuario.id_usuario}), 201

# Ruta para actualizar un usuario existente (Update - PUT)
@usuario_bp.route('/usuarios/actualizar', methods=['PUT'])
@auth_middleware
def actualizar_usuario(payload):
    usuario = Usuario.query.get_or_404(payload["id_usuario"])
    datos = request.get_json()

    # Actualizar los datos del usuario si están presentes en el request
    usuario.email = datos.get('email', usuario.email)
    usuario.nombre = datos.get('nombre', usuario.nombre)
    usuario.apellido = datos.get('apellido', usuario.apellido)
    usuario.genero = datos.get('genero', usuario.genero)
    usuario.fecha_nac = datos.get('fecha_nac', usuario.fecha_nac)
    usuario.contrasena = datos.get('contrasena', usuario.contrasena)
    usuario.id_ciudad = datos.get('id_ciudad', usuario.id_ciudad)

    db.session.commit()

    return jsonify({'message': 'Usuario actualizado con éxito'}), 200



# Ruta para desactivar un usuario (Update - PUT)
@usuario_bp.route('/usuarios/desactivar', methods=['PUT'])
@auth_middleware
def desactivar_usuario(payload):
    # Buscar el usuario por su ID
    usuario = Usuario.query.get_or_404(payload["id_usuario"])

    # Cambiar el estado de 'activo' a 0 (desactivado)
    usuario.activo = 0

    # Registrar la fecha y hora actual en 'fecha_desactivacion'
    usuario.fecha_desactivacion = datetime.utcnow()

    # Guardar los cambios en la base de datos
    db.session.commit()
    id_usuario=payload["id_usuario"]
    return jsonify({
        'message': f"Usuario con ID {id_usuario} ha sido desactivado.",
        'fecha_desactivacion': usuario.fecha_desactivacion.strftime('%Y-%m-%d %H:%M:%S')  # Formato legible de la fecha
    }), 200

