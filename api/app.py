from app import create_app  # Importamos la función que crea nuestra aplicación

# Creamos la aplicación utilizando la función create_app() que configuramos en app/__init__.py
app = create_app()

if __name__ == '__main__':
    # Ejecutamos la aplicación Flask en modo debug para facilitar el desarrollo
    app.run(debug=True)
