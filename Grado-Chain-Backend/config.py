import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui-deberia-ser-larga-y-aleatoria' # ¡MUY IMPORTANTE!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://admin:Cvpbdd1..2022@bot-agend.cz4q84ygixlh.us-east-2.rds.amazonaws.com/gradochain_system' # Ajusta tu cadena de conexión MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuraciones de MultiChain (asegúrate que estas sigan siendo correctas)
    MULTICHAIN_RPC_HOST = os.environ.get('MULTICHAIN_RPC_HOST', '127.0.0.1')
    MULTICHAIN_RPC_PORT = int(os.environ.get('MULTICHAIN_RPC_PORT', 6500)) 
    MULTICHAIN_RPC_USER = os.environ.get('MULTICHAIN_RPC_USER', 'multichainrpc')
    MULTICHAIN_RPC_PASSWORD = os.environ.get('MULTICHAIN_RPC_PASSWORD', '9AtWN6bf1eMPqGvKTJt8jxpDhQucKRv7rKuQJhZq5iEr')
    # La línea conflictiva de SQLite 'SQLALCHEMY_DATABASE_URI = 'sqlite:///multichain_db.db'' HA SIDO ELIMINADA
    SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost:5000') # Añadir si es necesario