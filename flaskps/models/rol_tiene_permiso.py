from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey

class Rol_tiene_permiso(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    permiso_id = db.Column(db.Integer, ForeignKey("permiso.id"), nullable = False)
    rol_id = db.Column(db.Integer, ForeignKey("rol.id"), nullable = False)
    # db = None
    __tablename__ = 'rol_tiene_permiso'

    @classmethod
    def all(cls):
        sql = 'SELECT * FROM rol_tiene_permiso'
        cursor = cls.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        #verificar que no exista una relacion entre ese rol y permiso / hacerlo en el controlador(del admn) mejor
        sql = """
            INSERT INTO rol_tiene_permiso (rol_id, permiso_id)
            VALUES (%s, %s)
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, list(data.values()))
        cls.db.commit()

        return True

    @classmethod
    def find_by_rol_id(cls, rol_id):
        sql = """
            SELECT * FROM rol_tiene_permiso AS u
            WHERE u.rol_id = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (rol_id))

        return cursor.fetchall()

    @classmethod
    def find_by_permiso_id(cls, permiso_id):
        sql = """
            SELECT * FROM rol_tiene_permiso AS u
            WHERE u.permiso_id = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (permiso_id))

        return cursor.fetchall() 

    @classmethod
    def find_permisos_by_rolId(cls, id_rol):
        permisos = Rol_tiene_permiso.query.filter_by(rol_id=id_rol).all()
        
        return [per.permiso_id for per in permisos]
        
        # sql = """
        #     SELECT * FROM rol_tiene_permiso AS u
        #     WHERE u.permiso_id = %s
        # """

        # cursor = cls.db.cursor()
        # cursor.execute(sql, (permiso_id))

        # return cursor.fetchall()        
