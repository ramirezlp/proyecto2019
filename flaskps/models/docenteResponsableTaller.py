from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey

class DocenteResponsableTaller(db.Model): 	
	id = db.Column(db.Integer, primary_key = True)
	docente_id = db.Column(db.Integer, db.ForeignKey("docente.id"))
	ciclo_lectivo_taller_id = db.Column(db.Integer, db.ForeignKey("ciclo_lectivo_taller.id"))
	__tablename__ = "docente_responsable_taller"

	def __init__(self, docenteId,  ciclo_lectivo_taller_id):
		self.docente_id = docenteId		
		self.ciclo_lectivo_taller_id = ciclo_lectivo_taller_id

	@classmethod
	def create(cls, docente, ciclo_lectivo_taller_id):
		dtc =  DocenteResponsableTaller(docente, ciclo_lectivo_taller_id)
		DocenteResponsableTaller.db.session.add(dtc)
		DocenteResponsableTaller.db.session.commit()
		return dtc

	@classmethod
	def delete(cls, id):
		rel = DocenteResponsableTaller.query.filter(DocenteResponsableTaller.id == id).first()
		DocenteResponsableTaller.db.session.delete(rel)
		DocenteResponsableTaller.db.session.commit()

	@classmethod
	def eliminar_responsables_taller_ciclo(cls,id):
		rels = DocenteResponsableTaller.query.filter(DocenteResponsableTaller.ciclo_lectivo_taller_id == id)
		for rel in rels:
			DocenteResponsableTaller.db.session.delete(rel)
		DocenteResponsableTaller.db.session.commit()
	@classmethod
	def find_by_docente_id_and_ciclo_lectivo_taller_id(cls, docente_id, ciclo_lectivo_taller_id):
		rel = DocenteResponsableTaller.query.filter(
			and_(DocenteResponsableTaller.docente_id == docente_id ,
			DocenteResponsableTaller.ciclo_lectivo_taller_id == ciclo_lectivo_taller_id)).first()
		return rel		

	@classmethod
	def find_by_ciclo_lectivo_taller_id(cls,id):
		docentes = DocenteResponsableTaller.query.filter(DocenteResponsableTaller.ciclo_lectivo_taller_id == id).all()
		return docentes

	@classmethod
	def find_by_docente_id(cls,id):
		rel = cls.query.filter(cls.docente_id == id).all()
		return rel