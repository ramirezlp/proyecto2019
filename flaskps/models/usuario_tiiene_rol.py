from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
class Usuario_tiene_rol(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, ForeignKey("users.id"), nullable = False)
    rol_id = db.Column(db.Integer, ForeignKey("rol.id"), nullable = False)
    __tablename__ = 'usuario_tiene_rol'
    #db = None

    def __init__(self, user_id, rol_id):
        self.usuario_id = user_id
        self.rol_id = rol_id
        
        # rel = usuario_tiene_rol()
        # rel.usuario_id = user_id
        # rel.rol_id = rol_id               

    @classmethod
    def all(cls):
        relaciones = Usuario_tiene_rol.query.all()
        '''
        sql = 'SELECT * FROM usuario_tiene_rol'
        cursor = cls.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
        '''
        return relaciones
    
    @classmethod
    def create(cls, data):
        rel = Usuario_tiene_rol(data)
        db.session.add(rel)
        db.session.commit()
        '''
        #verificar que no exista la relacion
        sql = """
            INSERT INTO usuario_tiene_rol (usuario_id, rol_id)
            VALUES (%s, %s)
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, list(data.values()))
        cls.db.commit()

        return True
        '''
    
    @classmethod
    def find_by_user(cls, usuario_id):
        relaciones = Usuario_tiene_rol.query.filter(Usuario_tiene_rol.usuario_id == usuario_id).all()
        '''
        sql = """
            SELECT * FROM usuario_tiene_rol AS u
            WHERE u.usuario_id = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (usuario_id))

        return cursor.fetchall()
        '''
        return relaciones

    @classmethod
    def find_by_rol_id(cls, rol_id):
        relaciones = Usuario_tiene_rol.query.filter(Usuario_tiene_rol.rol_id == rol_id).all()
        '''
        sql = """
            SELECT * FROM usuario_tiene_rol AS u
            WHERE u.rol_di = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (rol_di))

        return cursor.fetchall()   
        '''
        return relaciones
    @classmethod
    def find_by_user_and_rol(cls, usuario_id, rol_id):
        relaciones = Usuario_tiene_rol.query.filter(and_(Usuario_tiene_rol.usuario_id == usuario_id , Usuario_tiene_rol.rol_id == rol_id)).all()
        '''
        sql = """
            SELECT * FROM usuario_tiene_rol AS u
            WHERE u.usuario_id = %s AND u.rol_id = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (usuario_id, rol_id))

        return cursor.fetchall()     
        '''
        return relaciones
    @classmethod
    def delete_rol_usuario(cls, user_id,rol_id):
        relacion = Usuario_tiene_rol.query.filter(and_(Usuario_tiene_rol.usuario_id == user_id, Usuario_tiene_rol.rol_id == rol_id)).first()
        print(relacion)
        db.session.delete(relacion)
        db.session.commit()
        '''
        #verificar que no exista la relacion
        cursor = cls.db.cursor()
        sql = """
           DELETE FROM usuario_tiene_rol WHERE usuario_id = %s and rol_id = %s
        """
        cursor.execute(sql, (user_id,rol_id))
        cls.db.commit()

        return True
        '''
        return True
    @classmethod
    def insertar_rol(cls, user_id, rol_id):
        relacion = Usuario_tiene_rol.query.filter(and_(Usuario_tiene_rol.usuario_id == user_id, Usuario_tiene_rol.rol_id == rol_id)).first()
        if not relacion:
            relacion = Usuario_tiene_rol(user_id, rol_id)
            db.session.add(relacion)
            db.session.commit()
        return True            
        '''
        #verificar que no exista la relacion
        cursor = cls.db.cursor()
        sql = """
           INSERT INTO usuario_tiene_rol (usuario_id,rol_id)
           SELECT %s,%s FROM DUAL
           WHERE NOT EXISTS (
                SELECT * FROM usuario_tiene_rol WHERE usuario_id = %s and rol_id = %s
            )
        """
        cursor.execute(sql, (user_id,rol_id,user_id,rol_id))
        cls.db.commit()

        return True
        '''        