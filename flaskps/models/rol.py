from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
class Rol(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(255))
    #db = None
    __tablename__ = 'rol'

    def __init__(nombre):
        self.nombre = nombre

    @classmethod
    def all(cls):
        roles = Rol.query.all()
        '''
        sql = 'SELECT * FROM rol'
        cursor = cls.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
        '''
        return roles
    @classmethod
    def create(cls, data):
        rol = Rol(data.values())
        db.session.add(rol)
        db.session.commit()
        return True
        '''
        # verificar que el rol no se repita / hacerlo en el controlador(del admn) mejor 
        sql = """
            INSERT INTO rol (nombre)
            VALUES (%s)
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, list(data.values()))
        cls.db.commit()

        return True
        '''
    @classmethod
    def find_by_rol_id(cls, rol_id):
        rol = Rol.query.filter(Rol.id == rol_id).first()
        '''
        sql = """
            SELECT * FROM rol AS r
            WHERE r.rol_id = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (rol_id))

        return cursor.fetchone()
        '''
        return rol
    @classmethod
    def find_by_rol_name(cls, nombre):
        rol = Rol.query.filter(Rol.nombre == nombre).first()
        '''
        sql = """
            SELECT * FROM rol AS r
            WHERE r.nombre = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (nombre))

        return cursor.fetchone() 
        '''
        return rol
    @classmethod
    def find_by_rol_ids(cls, l):
        print (l)
        roles = Rol.query.filter(Rol.id.in_((l))).all()
        print (roles)

        return roles
        # if len(l) == 0:
        #     l.append(-1)
        # placeholders= ', '.join(['%s']*len(l))  # "%s, %s, %s, ... %s"
        # sql = 'SELECT nombre FROM rol WHERE rol.id IN ({})'.format(placeholders)
        # cursor = cls.db.cursor()
        # cursor.execute(sql, tuple(l))

        # return cursor.fetchall()       
