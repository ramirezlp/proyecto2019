from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey



class TipoInstrumento(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(255))
    __tablename__='tipo_instrumento'

class Instrumento(db.Model):
    numero_inventario = db.Column(db.String(255), primary_key=True)
    nombre = db.Column(db.String(255))
    tipo_instrumento_id = db.Column(db.Integer, ForeignKey("tipo_instrumento.id"), nullable = True)
    tipo_instrumento = db.relationship(TipoInstrumento, backref='instrumento')
    imagen=db.Column(db.String(255),nullable=True)

    __tablename__='instrumento'

    def serialize(self):
        return {
        'numero_inventario': self.numero_inventario,
        'nombre': self.nombre,
        'tipo_instrumento_id': self.tipo_instrumento_id,
        'imagen' : self.imagen
        } 