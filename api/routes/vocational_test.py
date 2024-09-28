from flask import request, jsonify, abort
from api import db
from api.models import TestVocacional, Usuario
from datetime import datetime
import json
from api.middleware.auth import auth_middleware
from flask import Blueprint


# Definimos un blueprint para las rutas relacionadas con el test vocacional
vocational_test_bp = Blueprint('vocational_test_bp', __name__)

# Ruta para enviar los resultados de la encuesta habiendose logeado (POST)
@vocational_test_bp.route('/encuesta', methods=['POST'])
@auth_middleware
def enviar_encuesta(payload):
    # Obtener el ID del usuario desde el payload del token
    id_usuario = payload['id_usuario']
    
    # Obtener las respuestas desde el cuerpo de la solicitud
    datos = request.get_json()
    
    if 'respuestas_usuario' not in datos:
        abort(400, description="Faltan las respuestas del usuario")
    
    # Convertir las respuestas del usuario a formato JSON
    respuestas_json = json.dumps(datos['respuestas_usuario'])
    
    # Crear un nuevo test vocacional
    nuevo_test = TestVocacional(
        fecha_realizacion=datetime.utcnow(),
        perfil_vocacional='Perfil por definir',  # Puedes calcular el perfil aquí si es necesario
        respuestas_test=respuestas_json,
        id_usuario=id_usuario  # Relacionar con el usuario autenticado
    )
    
    # Guardar en la base de datos
    db.session.add(nuevo_test)
    db.session.commit()
    
    # Respuesta exitosa
    return jsonify({
        'message': 'Encuesta enviada con éxito',
        'id_test': nuevo_test.id_test
    }), 201

#SIN LOGEARSE

# Ruta para enviar los resultados de la encuesta SIN LOGEARSE (POST)
@vocational_test_bp.route('/encuesta_sin_login', methods=['POST'])
def enviar_encuesta_unlogged():
    
    # Obtener las respuestas desde el cuerpo de la solicitud
    datos = request.get_json()
    
    if 'respuestas_usuario' not in datos:
        abort(400, description="Faltan las respuestas del usuario")
    
    # Convertir las respuestas del usuario a formato JSON
    respuestas_json = json.dumps(datos['respuestas_usuario'])
    
    # Crear un nuevo test vocacional
    nuevo_test = TestVocacional(
        fecha_realizacion=datetime.utcnow(),
        perfil_vocacional='Perfil por definir',  # Puedes calcular el perfil aquí si es necesario
        respuestas_test=respuestas_json
    )
    
    # Guardar en la base de datos
    db.session.add(nuevo_test)
    db.session.commit()
    
    # Respuesta exitosa
    return jsonify({
        'message': 'Encuesta enviada con éxito',
        'id_test': nuevo_test.id_test
    }), 201

    # Ruta para listar los resultados de la encuesta del usuario autenticado (GET)
    #Cuando una persona sin loggearse haga el test, podrá ver solo esa respuesta
    # y el historial/respuesta de la ultima realizada.
    #Si una persona se registró y logeó, podra ver todo el historial 
    # de sus encuestas desde que esta logeado y las respuestas obtenidas hacia el pasado.
@vocational_test_bp.route('/encuesta/listar', methods=['GET'])
@auth_middleware
def listar_encuestas(payload):
    # Obtener el ID del usuario desde el payload del token
    id_usuario = payload['id_usuario']
    
    # Obtener todos los tests vocacionales realizados por el usuario
    tests = TestVocacional.query.filter_by(id_usuario=id_usuario).all()
    
    # Si el usuario no tiene encuestas, devolver un mensaje
    if not tests:
        return jsonify({'message': 'No hay encuestas enviadas por este usuario'}), 404
    
    # Formatear los resultados en una lista
    resultados = []
    for test in tests:
        resultados.append({
            'id_test': test.id_test,
            'fecha_realizacion': test.fecha_realizacion.strftime('%Y-%m-%d %H:%M:%S'),
            'perfil_vocacional': test.perfil_vocacional,
            'respuestas_test': json.loads(test.respuestas_test)
        })
    
    return jsonify(resultados), 200