from api import db
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime

# Modelo Carrera
class Carrera(db.Model):
    __tablename__ = 'carreras'  
    id_carrera = db.Column(db.Integer, primary_key=True)
    codigo_carrera = db.Column(db.String(100))  
    nombre_carrera = db.Column(db.String(150), nullable=False)
    area_carrera = db.Column(db.String(100))
    subarea_carrera = db.Column(db.String(100))
    duracion_carrera = db.Column(db.Integer)
    nivel_global = db.Column(db.String(100))  
    nivel_academico = db.Column(db.String(100))  
    nombre_instituto = db.Column(db.String(150))  
    jornada = db.Column(db.String(100))  
    modalidad = db.Column(db.String(100))  
    nombre_sede = db.Column(db.String(150))  
    sede_comuna = db.Column(db.String(100))  
    acreditacion = db.Column(db.String(100))  
    salario_promedio = db.Column(db.Numeric(10, 2))
    empleabilidad = db.Column(db.Numeric(5, 2))

# Modelo Noticias
class Noticias(db.Model):
    __tablename__ = 'noticias'

    id_noticia = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    link_noticia = db.Column(db.String(255), nullable=True)
    imagen_noticia = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id_noticia': self.id_noticia,
            'titulo': self.titulo,
            'contenido': self.contenido,
            'fecha_publicacion': self.fecha_publicacion.isoformat(),  # Convertir fecha a formato JSON
            'link_noticia': self.link_noticia,
            'imagen_noticia': self.imagen_noticia
        }

# Modelo Región
class Region(db.Model):
    __tablename__ = 'region'
    id_region = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)

# Modelo Ciudad
class Ciudad(db.Model):
    __tablename__ = 'ciudad'
    id_ciudad = db.Column(db.Integer, primary_key=True)
    ciudad = db.Column(db.String(100), nullable=False)
    id_region = db.Column(db.Integer, db.ForeignKey('region.id_region'))

    # Relación con la tabla Region
    region = db.relationship('Region', backref='ciudades')

# Modelo Usuario
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(10))
    fecha_nac = db.Column(db.Date)
    contrasena = db.Column(db.String(200), nullable=False)
    id_ciudad = db.Column(db.Integer, db.ForeignKey('ciudad.id_ciudad'))
    activo = db.Column(db.Integer)
    ultimo_login = db.Column(db.DateTime)
    ultima_actualizacion = db.Column(db.DateTime)
    creacion_usuario = db.Column(db.DateTime)
    fecha_desactivacion = db.Column(db.DateTime)
    suscripcion_boletin = db.Column(db.Integer, default=0)

    # Relación con la tabla Región
    ciudad = db.relationship('Ciudad', backref='usuarios')
    

# Modelo Test Vocacional
class TestVocacional(db.Model):
    __tablename__ = 'test_vocacional'
    id_test = db.Column(db.Integer, primary_key=True)
    fecha_realizacion = db.Column(db.DateTime, nullable=False)  # Cambiado a DateTime para almacenar fecha y hora    # Cambiar perfil_vocacional a LONGTEXT
    perfil_vocacional = db.Column(LONGTEXT)  # Se ajusta a LONGTEXT para almacenar perfiles más largos o en formato JSON
    # Nuevo campo respuestas_test también como LONGTEXT
    respuestas_test = db.Column(LONGTEXT, nullable=True)  # Campo para almacenar las respuestas del test
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    # Relación con la tabla Usuario
    usuario = db.relationship('Usuario', backref='tests_vocacionales')

# Modelo Recomendación
class Recomendacion(db.Model):
    __tablename__ = 'recomendacion'
    id_recomendacion = db.Column(db.Integer, primary_key=True)
    fecha_recomendacion = db.Column(db.Date, nullable=False)
    id_test = db.Column(db.Integer, db.ForeignKey('test_vocacional.id_test'))
    id_carrera = db.Column(db.Integer, db.ForeignKey('carreras.id_carrera'))

    # Relaciones con TestVocacional y Carrera
    test = db.relationship('TestVocacional', backref='recomendaciones')
    carrera = db.relationship('Carrera', backref='recomendaciones')

# Modelo Feedback
class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id_feedback = db.Column(db.Integer, primary_key=True)
    puntuacion = db.Column(db.Integer, db.CheckConstraint('puntuacion BETWEEN 1 AND 5'))
    comentario = db.Column(db.String(500))
    fecha_feedback = db.Column(db.DateTime)
    id_recomendacion = db.Column(db.Integer, db.ForeignKey('recomendacion.id_recomendacion'))
    
    # Nueva columna para la relación con Usuario
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))  
    
    # Relación con el modelo Usuario
    usuario = db.relationship('Usuario', backref='feedbacks')



    # Relación con Recomendación
    recomendacion = db.relationship('Recomendacion', backref='feedbacks')


  # Modelo Boletin Informativo
class BoletinInformativo(db.Model):
    __tablename__ = 'boletin_informativo'
    
    id_boletin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fuente = db.Column(db.String(255))
    link_mas_informacion = db.Column(db.String(255))
    fecha_envio = db.Column(db.Date, default=datetime.utcnow)