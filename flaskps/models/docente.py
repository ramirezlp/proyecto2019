from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
from flaskps.models.estudiante import Genero

class Docente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellido = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    fecha_nac = db.Column(db.DateTime)
    localidad_id= db.Column(db.Integer)
    domicilio = db.Column(db.String(255))
    genero_id = db.Column(db.Integer, ForeignKey("genero.id"))
    genero = db.relationship(Genero, backref='docente')
    tipo_doc_id = db.Column(db.Integer)
    numero_documento = db.Column(db.Integer)
    tel = db.Column(db.String(255), nullable=True)

    __tablename__='docente'

    def __init__(self, nombre, apellido, telefono, fecha_nac, localidad, domicilio, genero, tipo_doc, num_doc):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nac = fecha_nac
        self.localidad_id = localidad
        self.domicilio = domicilio
        self.genero_id = genero
        self.tipo_doc_id = tipo_doc
        self.numero_documento = num_doc
        self.tel = telefono

    def serialize(self):
        return {
            'id': self.id,
            'apellido': self.apellido,
            'nombre': self.nombre,
            'fecha_nacimiento': self.fecha_nac,
            'localidad_id': self.localidad_id,
            'domicilio': self.domicilio,
            'genero': self.genero.nombre,
            'genero_id': self.genero_id,
            'tipo_doc_id': self.tipo_doc_id,
            'documento': self.numero_documento,
            'telefono': self.tel,
        }

    @classmethod
    def all(cls):
        docentes = Docente.query.all()
        return docentes