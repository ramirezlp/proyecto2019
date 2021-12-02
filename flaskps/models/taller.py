from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
from flaskps.models.cicloLectivo import CicloLectivo
from flaskps.models import cicloLectivoTaller as clt
from datetime import datetime

class Taller(db.Model):    
	id = db.Column(db.Integer, primary_key = True)    
	nombre = db.Column(db.String(255))
	nombre_corto = db.Column(db.String(255))
	__tablename__ = "taller"

	def __init__(self, nombre, nombrecorto):
		self.nombre = nombre
		self.nombre_corto = nombrecorto    

	@classmethod
	def create(cls, nombre, nombreCorto):
		taller = Taller(nombre, nombreCorto)
		Taller.db.session.add(taller)
		Taller.db.session.commit()
		return taller

	@classmethod
	def find_by_id(cls,id):
		taller = Taller.query.filter(Taller.id == id).first()
		return taller

	def es_dia_asistencia(self, ciclo_lectivo_taller_id):
		dicdias = {'MONDAY':'lunes','TUESDAY':'martes','WEDNESDAY':'miercoles','THURSDAY':'jueves', \
				'FRIDAY':'viernes','SATURDAY':'sabado','SUNDAY':'domingo'}
		try:
			horarios_taller = [clth.horario_id for clth in clt.CicloLectivoTallerHorario.query.filter_by(ciclo_lectivo_taller_id=ciclo_lectivo_taller_id).all()]
			horarios_taller = [clt.Horario.query.filter_by(id=horario).first().dia for horario in horarios_taller]
			if dicdias[datetime.now().strftime("%A").upper()] in horarios_taller:
				return True
		except:
			return False
		return False

class Nucleo(db.Model):
	id = db.Column(db.Integer, primary_key = True)    
	nombre = db.Column(db.String(255))
	direccion = db.Column(db.String(255))
	telefono = db.Column(db.String(255))
	latitud = db.Column(db.Float(6),nullable = True)
	longitud = db.Column(db.Float(6),nullable = True)
	__tablename__ = "nucleo"

	def __init__(self, nombre, tel, direc):
		self.nombre = nombre
		self.telefono = tel
		self.direccion = direc

	def serialize(self):
		return {
        	'id': self.id,
			'nombre': self.nombre,
			'direccion': self.direccion,
			'telefono': self.telefono,
			'latitud': self.latitud,
			'longitud': self.longitud,			
			'toString': "Nombre: " + str(self.nombre) + " - Direccion: " + str(self.direccion)
		}

	@classmethod
	def create(cls, nombre, tel, direc):
		nucleo = Taller(nombre, tel, direc)
		Nucleo.db.session.add(nucleo)
		Nucleo.db.session.commit()
		return nucleo

	@classmethod
	def setCoords(cls,id,lat,lng):		
		nucleo = cls.query.filter(cls.id == id).first()	
		nucleo.latitud = float(lat)
		nucleo.longitud = float(lng)
		db.session.commit()
		return nucleo

	@classmethod
	def cleanCords(cls,id):
		nucleo = cls.query.filter(cls.id == id).first()	
		print(id)
		nucleo.latitud = None
		nucleo.longitud = None
		db.session.commit()
		return nucleo

	@classmethod
	def all(cls):
		nucleos =  cls.query.all()
		return nucleos		