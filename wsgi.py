from api import create_app  # Importamos la función create_app desde api/__init__.py

# Creamos la aplicación Flask
app = create_app()

if __name__ == "__main__":
    app.run()
