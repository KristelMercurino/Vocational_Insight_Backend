from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importa CORS
from dotenv import load_dotenv
import os

# Inicializamos SQLAlchemy
db = SQLAlchemy()

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Habilita CORS para todos los orígenes y soporta credenciales si es necesario
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Configuración de la base de datos con la URI proporcionada
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    # Definir la URI de conexión a la base de datos MariaDB
    DB_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Configurar la URI de la base de datos en la aplicación Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar advertencias de SQLAlchemy

    # Inicializamos la base de datos con la aplicación Flask
    db.init_app(app)

    # Registrar blueprints de rutas (por ejemplo, rutas de usuario)
    from api.routes.user import usuario_bp
    from api.routes.auth import auth_bp
    from api.routes.region import region_bp
    from api.routes.vocational_test import vocational_test_bp
    from api.routes.careers import careers_bp
    from api.routes.feedback import feedback_bp
    from api.routes.reset_password import reset_pass_bp
    from api.routes.news import news_bp
    from api.routes.newsletter import newsletter_bp
    from api.routes.subscription import suscription_bp

    app.register_blueprint(usuario_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(region_bp)
    app.register_blueprint(vocational_test_bp)
    app.register_blueprint(careers_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(reset_pass_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(newsletter_bp)
    app.register_blueprint(suscription_bp)

    return app