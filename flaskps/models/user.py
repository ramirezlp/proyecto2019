from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255),unique = True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))    
    last_name =db.Column(db.String(255))
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    activo = db.Column(db.Integer, default=1, nullable=False)
    username = db.Column(db.String(255), unique=True)
    # avatar = db.Column(db.String(200))
    # tokens = db.Column(db.Text)
    #db = None
    __tablename__ = 'users'
    
    def __init__(self, email, password, firstname, lastname, username):
        self.email = email
        self.password = password
        self.first_name =firstname
        self.last_name = lastname
        self.username = username

    @classmethod
    def all(cls):
        usuarios = User.query.all()
        '''
        sql = 'SELECT * FROM users'
        cursor = cls.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
        '''
        return usuarios
    @classmethod
    def find_by_name(cls, name):
        search = "%{}%".format(name)
        usuarios = User.query.filter(User.first_name.like(search)).all()
        print(usuarios)
        '''
        sql = 'SELECT * FROM users WHERE users.first_name LIKE %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, ("%" + name + "%"))

        return cursor.fetchall()
        '''
        return usuarios

    @classmethod
    def create(cls, email, password, firstname, lastname, username):    
        print("mnmolno")    
        usuario = User(email, password, firstname, lastname, username)
        db.session.add(usuario)
        db.session.commit()
        return True
        '''
        sql = """
            INSERT INTO users (email, password, first_name, last_name, username)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (email, password, firstname, lastname, username))
        cls.db.commit()

        return True
        '''
    @classmethod
    def find_by_email_and_pass(cls, email, password):
        usuario = User.query.filter(and_(User.email == email , User.password == password)).first()
        '''
        sql = """
            SELECT * FROM users AS u
            WHERE u.email = %s AND u.password = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (email, password))

        return cursor.fetchone()
        '''
        return usuario
    @classmethod
    def find_by_username_and_active(cls, text, num):
        search = "%{}%".format(text)
        usuarios = User.query.filter(and_(User.username.like(search) , User.activo == num))
        '''
        cursor = cls.db.cursor()
        cursor.execute("SELECT * FROM users WHERE users.username LIKE %s AND users.activo = %s", ("%" + text + "%", num))

        return list(cursor)
        '''
        return usuarios
    @classmethod
    def existing_username(cls, username):
        usuario = User.query.filter(User.username == username).first()
        '''
        sql = """
            SELECT * FROM users
            WHERE users.username = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (username))

        return cursor.fetchone()
        '''
        return usuario
    @classmethod
    def find_by_email(cls, email):
        usuario = User.query.filter(User.email == email).first()
        '''
        sql = """
            SELECT * FROM users AS u
            WHERE u.email = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (email))

        return cursor.fetchone()
        '''
        return usuario
    @classmethod
    def find_by_id(cls, id):
        usuario = User.query.filter(User.id == id).first()
        '''
        sql = """ 
            SELECT * FROM users AS u
            WHERE u.id = %s
        """
        cursor = cls.db.cursor()
        cursor.execute(sql, (id))
        return cursor.fetchone()
        '''
        return usuario

    @classmethod
    def act(cls, idn, email, password,activo, firstname, lastname, username):
        usuario = User.find_by_id(idn)
        usuario.email = email
        usuario.password = password
        usuario.first_name = firstname
        usuario.last_name = lastname
        usuario.id = idn
        db.session.commit()        
        return usuario
        '''
        sql = """
            UPDATE users AS u
                SET u.email = %s , u.username = %s , u.password = %s , u.activo = %s , u.first_name = %s , u.last_name = %s
            WHERE u.id = %s
        """        
        cursor = cls.db.cursor()
        cursor.execute(sql, (email, username, password, activo, firstname, lastname, idn))
        cls.db.commit()
        return cursor.fetchone()
        '''

    @classmethod
    def change_state(cls, id):
        usuario = User.find_by_id(id)
        usuario.activo = not usuario.activo
        db.session.commit()
        '''
        sql = """
            UPDATE users AS u
            SET u.activo = NOT u.activo
            WHERE u.id= %s
        """        
        cursor = cls.db.cursor()
        cursor.execute(sql, (id))
        cls.db.commit()
        '''
    @classmethod
    def find_by_name_and_active(cls, text, num):
        search = "%{}%".format(text)
        usuarios = User.query.filter(and_(User.first_name.like(search)), User.activo == num).all()
        return usuarios
        '''
        cursor = cls.db.cursor()
        cursor.execute("SELECT * FROM users WHERE users.first_name LIKE %s AND users.activo = %s", ("%" + text + "%", num))

        return list(cursor)
        '''

    @classmethod
    def delete(cls, user_id):
        usuario = User.find_by_id(user_id)
        db.session.delete(usuario)
        return True
        '''
        #verificar que no exista la relacion
        cursor = cls.db.cursor()
        sql = """
           DELETE FROM users WHERE id = %s
        """
        cursor.execute(sql, (user_id))
        cls.db.commit()
    
        return True
        '''
