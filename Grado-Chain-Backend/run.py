from app import create_app

# Crea la aplicación usando la fábrica
# Esto buscará app/__init__.py y llamará a create_app()
application = create_app() 

if __name__ == '__main__':
    # El puerto 5000 es donde tu API Flask escuchará.
    # El puerto de MultiChain (ej: 6500) es diferente y se usa internamente.
    application.run(debug=True, host='0.0.0.0', port=5000)