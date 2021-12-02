from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
from datetime import datetime

class CicloLectivo(db.Model):       
	id = db.Column(db.Integer, primary_key = True)    
	fecha_ini = db.Column(db.DateTime)
	fecha_fin = db.Column(db.DateTime)
	semestre = db.Column(db.Integer)
	__tablename__ = "ciclo_lectivo"

	def __init__(self, inicio, fin, semestre):
		self.fecha_ini = inicio
		self.fecha_fin = fin
		self.semestre = semestre      

	@classmethod
	def create(cls, inicio, fin, semestre):		
		ciclo = CicloLectivo(inicio, fin, semestre)
		CicloLectivo.db.session.add(ciclo)
		CicloLectivo.db.session.commit()

	@classmethod
	def update(cls,ciclo_id, inicio, fin, semestre):		
		ciclo = cls.find_by_id(ciclo_id)
		ciclo.fecha_ini = inicio
		ciclo.fecha_fin = fin
		ciclo.semestre = semestre
		CicloLectivo.db.session.commit()
		return ciclo

	@classmethod
	def find_by_id(cls,id):
		ciclo = CicloLectivo.query.filter(CicloLectivo.id == id).first()		
		return ciclo

	@classmethod
	def find_by_fecha_inicio_y_semestre(cls,inicio,semestre):
		ciclo = CicloLectivo.query.filter(and_(CicloLectivo.fecha_ini == inicio , CicloLectivo.semestre == semestre)).first()
		return ciclo
	@classmethod
	def all(cls):
		ciclos = CicloLectivo.query.all()
		return ciclos

	@classmethod		
	def delete(cls,id):
		CicloLectivo.query.filter(CicloLectivo.id == id).delete()
		CicloLectivo.db.session.commit()
"""
un estudiante pertenece a uno o muchos talleres, en uno o muchos ciclos lectivos

relaciones: estudiante taller/ciclo -> many to many bidireccional

dado un estudiante:

	quiero saber en que talleres participa,
	quiero saber en que talleres participo,

dado un taller:

	quiero saber que estudiantes participan,
	quiero saber que estudiantes participaron,
	quiero saber quienes son los reponsables,
	quiero saber quienes fueron los responsables,

dado un docente:
	quiero saber en que talleres es responsable,
	quiero saber en que talleres fue responsable,

"""		