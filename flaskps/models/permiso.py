from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

class Permiso(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    # db = None
    __tablename__ = 'permiso'

    def __init__(self, nombre):
        self.nombre = nombre
        
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM permiso'
        cursor = cls.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        #verificar que no exista el usuario/ hacerlo en el controlador mejor
        sql = """
            INSERT INTO permiso (nombre)
            VALUES (%s)
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, list(data.values()))
        cls.db.commit()

        return True

    @classmethod
    def find_by_nombre(cls, aNombre):
        permiso = Permiso.query.filter_by(nombre=aNombre).first()
        return permiso
    