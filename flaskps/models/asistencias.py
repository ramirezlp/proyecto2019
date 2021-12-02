from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
from datetime import datetime

class DiaSemana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(255))
    __tablename__ = 'dia_semana'

class ClaseTallerCicloLectivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taller_ciclo_lectivo_id = db.Column(db.Integer, db.ForeignKey("ciclo_lectivo_taller.id"))
    dia_semana = db.Column(db.Integer, db.ForeignKey("dia_semana.id"))
    __tablename__ = 'clase_taller_ciclo_lectivo'

class AsistenciaTallerCicloLectivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ciclo_lectivo_taller_horario = db.Column(db.Integer, db.ForeignKey("ciclo_lectivo_taller_horario.id")) 
    estudiante_id = db.Column(db.Integer, db.ForeignKey("estudiante.id"))
    dia = db.Column(db.DateTime)
    __tablename__='asistencia_taller_ciclo_lectivo_dia'