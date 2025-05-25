from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Modelo de base de datos para almacenar publicaciones
class StreamPublication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stream_name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)
    txid = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<StreamPublication {self.stream_name}>"

# Función para interactuar con MultiChain vía RPC
def call_multichain_rpc(method, params=[]):
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        f"http://{app.config['MULTICHAIN_RPC_HOST']}:{app.config['MULTICHAIN_RPC_PORT']}",
        auth=(app.config['MULTICHAIN_RPC_USER'], app.config['MULTICHAIN_RPC_PASSWORD']),
        json=payload
    )
    return response.json()

# Endpoint para listar streams
@app.route('/api/streams', methods=['GET'])
def get_streams():
    try:
        streams = call_multichain_rpc("liststreams")['result']
        return jsonify({"streams": streams}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para publicar datos en un stream
@app.route('/api/publish/<stream_name>', methods=['POST'])
def publish_to_stream(stream_name):
    try:
        data = request.json.get('data')
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Convertir los datos a formato hexadecimal (requerido por MultiChain)
        data_hex = data.encode('utf-8').hex()
        
        # Publicar en el stream
        result = call_multichain_rpc("publish", [stream_name, "key1", data_hex])
        if 'error' in result and result['error']:
            return jsonify({"error": result['error']['message']}), 500
        
        # Obtener el txid de la transacción
        txid = result.get('result')
        
        # Guardar en la base de datos
        publication = StreamPublication(stream_name=stream_name, data=data, txid=txid)
        db.session.add(publication)
        db.session.commit()
        
        return jsonify({"message": "Published successfully", "txid": txid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para consultar publicaciones de un stream (opcional)
@app.route('/api/publications/<stream_name>', methods=['GET'])
def get_publications(stream_name):
    try:
        publications = StreamPublication.query.filter_by(stream_name=stream_name).all()
        return jsonify({
            "stream_name": stream_name,
            "publications": [{"data": pub.data, "txid": pub.txid} for pub in publications]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

with app.app_context():
    db.create_all()  # Crea la base de datos si no existe

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)