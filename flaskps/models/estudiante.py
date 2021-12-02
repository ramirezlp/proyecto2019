from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
from flaskps.models.cicloLectivoTaller import CicloLectivoTallerHorario, Horario
from flaskps.models.asistencias import AsistenciaTallerCicloLectivo

class Barrio(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    nombre= db.Column(db.String(255))
    __tablename__='barrio'

class Genero(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    nombre= db.Column(db.String(255))
    __tablename__='genero'

class Responsable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellido = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    fecha_nacimiento = db.Column(db.DateTime)
    lugar_de_nacimiento = db.Column(db.String(255))
    localidad_id= db.Column(db.Integer)
    domicilio = db.Column(db.String(255))
    genero_id = db.Column(db.Integer, ForeignKey("genero.id"), nullable = False)
    tipo_doc_id = db.Column(db.Integer)
    documento = db.Column(db.Integer)  
    __tablename__='responsable'

class Nivel(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(255))
    __tablename__='nivel'

class Escuela(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(255))

    __tablename__='escuela'


class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellido = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    fecha_nacimiento = db.Column(db.DateTime)
    lugar_de_nacimiento = db.Column(db.String(255), nullable=True)
    localidad_id= db.Column(db.Integer)
    domicilio = db.Column(db.String(255))
    genero_id = db.Column(db.Integer, ForeignKey("genero.id"), nullable = True)
    genero = db.relationship(Genero, backref='estudiante')
    barrio_id = db.Column(db.Integer, ForeignKey("barrio.id"), nullable = True)
    barrio = db.relationship(Barrio, backref='estudiante')
    tipo_doc_id = db.Column(db.Integer)
    documento = db.Column(db.Integer)
    telefono= db.Column(db.String(255), nullable=True)
    responsable= db.Column(db.String(255))
    escuela_id = db.Column(db.Integer, ForeignKey("escuela.id"), nullable = True)
    escuela = db.relationship(Escuela, backref='estudiante')
    nivel_id = db.Column(db.Integer, ForeignKey("nivel.id"), nullable = True)
    nivel = db.relationship(Nivel, backref='estudiante')
    numero_contacto = db.Column(db.Integer)
    email_contacto = db.Column(db.String(255))

    __tablename__='estudiante'

    def serialize(self):
        return {
        'id': self.id,
        'apellido': self.apellido,
        'nombre': self.nombre,
        'fecha_nacimiento': self.fecha_nacimiento,
        'lugar_de_nacimiento': self.lugar_de_nacimiento,
        'localidad_id': self.localidad_id,
        'domicilio': self.domicilio,
        'genero': self.genero.nombre,
        'genero_id': self.genero_id,
        'barrio': self.barrio.nombre,
        'barrio_id': self.barrio_id,
        'tipo_doc_id': self.tipo_doc_id,
        'documento': self.documento,
        'telefono': self.telefono,
        'escuela': self.escuela.nombre,
        'escuela_id': self.escuela_id,
        'nivel': self.nivel.nombre,
        'nivel_id':self.nivel_id,
        'responsable': self.responsable,
        'numero_contacto': self.numero_contacto,
        'email_contacto': self.email_contacto
        }

    def chequear_asistencia(self,ciclo_lectivo_taller):
        import datetime
        dicdias = {'MONDAY':1,'TUESDAY':2,'WEDNESDAY':3,'THURSDAY':4, \
		'FRIDAY':5,'SATURDAY':6,'SUNDAY':7}
        dia = dicdias[datetime.datetime.now().strftime("%A").upper()]
        taller_horario = CicloLectivoTallerHorario.query.filter_by(ciclo_lectivo_taller_id=ciclo_lectivo_taller,horario_id=dia).first()
        asistencias = AsistenciaTallerCicloLectivo.query.filter_by(ciclo_lectivo_taller_horario=taller_horario.id, estudiante_id=self.id)
        asistencia_final = []
        for asistencia in asistencias:
            if asistencia.dia.strftime("%m/%d/%Y") == datetime.datetime.now().strftime("%m/%d/%Y"):
                asistencia_final.append(asistencia)
        print('asistencias: ',asistencias)
        return asistencia_final

class ResponsableEstudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    responsable_id = db.Column(db.Integer, ForeignKey("responsable.id"), nullable = False)
    estudiante_id = db.Column(db.Integer, ForeignKey("estudiante.id"), nullable = False)
    __tablename__='responsable_estudiante'  

