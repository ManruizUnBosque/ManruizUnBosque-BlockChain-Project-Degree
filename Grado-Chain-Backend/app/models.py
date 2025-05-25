from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StreamPublication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stream_name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)
    txid = db.Column(db.String(100), nullable=True)
    qr_code_url = db.Column(db.String(255), nullable=True) 

    def __repr__(self):
        return f"<StreamPublication {self.stream_name}>"

# NO AÑADIR la clase Documento aquí