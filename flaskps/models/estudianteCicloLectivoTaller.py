from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from datetime import datetime

class EstudianteCicloLectivoTaller(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	estudiante_id = db.Column(db.Integer, ForeignKey("estudiante.id"))
	ciclo_lectivo_taller_id = db.Column(db.Integer, ForeignKey("ciclo_lectivo_taller.id"))
	__table_name__ = "estudiante_ciclo_lectivo_taller"

	def __init__(self, estudiante, ciclo_taller):
		self.estudiante_id = estudiante
		self.ciclo_lectivo_taller_id = ciclo_taller

	@classmethod
	def create(cls,estudiante, ciclo_taller):
		rel = cls(estudiante,ciclo_taller)
		cls.db.session.add(rel)
		cls.db.session.commit()
		return rel
	
	@classmethod
	def update(cls, id, estudiante, ciclo_taller):
		rel = cls.query.filter(cls.id == id).first()
		rel.estudiante_id = estudiante
		rel.estudiante_ciclo_lectivo_taller_id = ciclo_taller
		cls.db.session.commit()
		return rel

	@classmethod
	def delete(cls,id):
		rel = cls.query.filter(cls.id == id).first()
		cls.db.session.delete(rel)
		cls.db.session.commit()
		return True

	@classmethod
	def find_by_estudiante_id(cls,id):
		rel = cls.query.filter(cls.estudiante_id == id).all()
		return rel
	

	@classmethod
	def find_by_estudiante_id_and_ciclo_lectivo_taller_id(cls,es,ta):
		rel = cls.query.filter(and_(cls.estudiante_id == es , cls.ciclo_lectivo_taller_id == ta)).first()
		return rel

	@classmethod
	def find_by_ciclo_lectivo_taller_id(cls,id):
		rel = cls.query.filter(cls.ciclo_lectivo_taller_id == id).all()
		return rel

	@classmethod
	def eliminar_estudiantes_taller_ciclo(cls,id):
		rels = cls.query.filter(cls.ciclo_lectivo_taller_id == id)
		for rel in rels:
			cls.db.session.delete(rel)
			cls.db.session.commit()		
				

