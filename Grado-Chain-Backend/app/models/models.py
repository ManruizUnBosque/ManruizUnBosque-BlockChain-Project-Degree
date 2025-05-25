from .. import db  # Imports db from app/__init__.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from datetime import datetime # Uncomment if you use DateTime fields

class StreamPublication(db.Model):
    __tablename__ = 'stream_publication'
    id = db.Column(db.Integer, primary_key=True)
    stream_name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)
    txid = db.Column(db.String(100), nullable=True)
    qr_code_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<StreamPublication {self.stream_name}>"

class Documento(db.Model):
    __tablename__ = 'documento'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    ruta = db.Column(db.String(512), nullable=False)  # Stores URL or file path
    hash_sha256 = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Documento {self.nombre}>"


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Aumentado para hashes más largos
    role = db.Column(db.String(20), nullable=False, default='estudiante')  # Roles: estudiante, profesor, directivo

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'