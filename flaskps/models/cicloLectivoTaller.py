from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
from flaskps.models.cicloLectivo import CicloLectivo
from flaskps.models.taller import Taller ###
class CicloLectivoTaller(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	taller_id = db.Column(db.Integer, db.ForeignKey("taller.id"))
	ciclo_lectivo_id = db.Column(db.Integer, db.ForeignKey("ciclo_lectivo.id"))
	nucleo_id = db.Column(db.Integer, db.ForeignKey("nucleo.id"),nullable=True)
	ciclo_lectivo_taller_horario_id = db.Column(db.Integer, db.ForeignKey("ciclo_lectivo_taller_horario.id"),nullable=True)
	__tablename__ = "ciclo_lectivo_taller"

	def __init__(self, taller, ciclo):
		self.taller_id = taller
		self.ciclo_lectivo_id = ciclo

	def serialize(self):
		return {
        	'id': self.id,
			'taller_id': self.taller_id,
			'ciclo_lectivo_id': self.ciclo_lectivo_id,
			'toString': "Semestre: " + str(self.nombreCiclo().semestre) + " - Nombre: " + str(self.nombreTaller().nombre_corto)
		}

	def nombreTaller(self):
		return Taller.query.filter(Taller.id == self.taller_id).first()
		# return Taller.query(Taller.nombre_corto).filter(Taller.id == self.taller_id).first()

	def nombreCiclo(self):
		return CicloLectivo.query.filter(CicloLectivo.id == self.ciclo_lectivo_id).first()

	@classmethod
	def delete(cls,id):
		rel = cls.find_by_id(id)
		cls.db.session.delete(rel)
		cls.db.session.commit()

	@classmethod
	def create(cls, taller, ciclo):
		rel = CicloLectivoTaller(taller, ciclo)
		CicloLectivoTaller.db.session.add(rel)
		CicloLectivoTaller.db.session.commit()
		return rel

	@classmethod
	def find_by_taller_id(cls,id):
		ciclos = CicloLectivoTaller.query.filter(CicloLectivoTaller.taller_id ==id).all()
		return ciclos	

	@classmethod
	def find_by_taller_id_and_ciclo_id(cls, taller_id, ciclo_id):
		ciclos = CicloLectivoTaller.query.filter(and_(CicloLectivoTaller.taller_id == taller_id , CicloLectivoTaller.ciclo_lectivo_id == ciclo_id)).first()
		return ciclos
	@classmethod
	def find_by_id(cls,id):
		rel = cls.query.filter(cls.id == id).first()
		return rel

	@classmethod
	def find_by_ciclo_lectivo_id(cls,id):
		rels = cls.query.filter(cls.ciclo_lectivo_id == id).all()
		return rels

class CicloLectivoTallerHorario(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ciclo_lectivo_taller_id = db.Column(db.Integer, db.ForeignKey("ciclo_lectivo_taller.id"))
	horario_id = db.Column(db.Integer, db.ForeignKey("horario.id"))
	__tablename__ ="ciclo_lectivo_taller_horario"

	def __init__(self, clt, horario_id):
		self.ciclo_lectivo_taller_id = clt
		self.horario_id = horario_id


class Horario(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	dia = db.Column(db.String(255))
	__tablename__ ="horario"

	def __init__(self, dia):
		self.dia = dia

	def serialize(self):
		return {
        	'id': self.id,
			'dia': self.dia
		}