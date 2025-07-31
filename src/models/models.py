from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Dueno(db.Model):
    __tablename__ = 'duenos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con perros
    perros = db.relationship('Perro', backref='dueno', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Dueno {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'perros': [perro.nombre for perro in self.perros]
        }

class Perro(db.Model):
    __tablename__ = 'perros'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    tamano = db.Column(db.Enum('Pequeño', 'Mediano', 'Grande', name='tamano_enum'), nullable=False)
    comportamiento = db.Column(db.String(200))
    calle = db.Column(db.String(200))
    edad = db.Column(db.Integer)
    dueno_id = db.Column(db.Integer, db.ForeignKey('duenos.id'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Perro {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'raza': self.raza,
            'tamano': self.tamano,
            'comportamiento': self.comportamiento,
            'calle': self.calle,
            'edad': self.edad,
            'dueno_id': self.dueno_id,
            'dueno_nombre': self.dueno.nombre if self.dueno else None,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

