# Import the db instance from the parent package (app/__init__.py)
from .. import db

# Import model classes from .models (i.e., app/models/models.py)
from .models import StreamPublication, Documento, User # Añadir User aquí

# Make db and models available for import like: from app.models import db, StreamPublication
__all__ = ['db', 'StreamPublication', 'Documento', 'User'] # Añadir User aquí