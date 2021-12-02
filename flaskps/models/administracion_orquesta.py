from flaskps.models.shared import db
from flask_sqlalchemy import SQLAlchemy
class AdministracionOrquesta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    mail_contacto = db.Column(db.String(255))
    sitio_activo = db.Column(db.Boolean)
    elementos_por_pagina = db.Column(db.Integer)
    created = db.Column(db.Date)
    __tablename__="administracion_orquesta"
#    db = None

    def __init__(titulo,descripcion,mail_contacto,sitio_activo,elementos_por_pagina):
        self.titulo = titulo
        self.descripcion = descripcion
        self.mail_contacto = mail_contacto
        self.sitio_activo = sitio_activo
        self.elementos_por_pagina = elementos_por_pagina
        self.created = None        

    @classmethod
    def create(cls, data):
        # verificar que el rol no se repita / hacerlo en el controlador(del admn) mejor 
        adm = AdministracionOrquesta(list(data.values))
        db.session.add(adm)
        db.session.commit()
        '''
        sql = """
            INSERT INTO administracion_orquesta (titulo,descripcion,mail_contacto,sitio_activo,elementos_por_pagina)
            VALUES (%s)
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, list(data.values()))
        cls.db.commit()
        '''
        return True


    @classmethod
    def find_by_administracion_titulo(cls, Titulo):
        adm = AdministracionOrquesta.query.filter_by(titulo = Titulo).first()
        return adm
        '''
        sql = """
            SELECT * FROM administracion_orquesta AS a
            WHERE a.titulo = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (nombre))

        return cursor.fetchone()
        '''
    @classmethod
    def activar_desactivar_sitio(cls,activar):
        # adm = cls.get()
        AdministracionOrquesta.query.filter_by(id=1).first().sitio_activo = activar
        db.session.commit()
        '''
        sql = """
               UPDATE administracion_orquesta AS s
               SET s.sitio_activo = %s 
               WHERE s.id = 1;
            """
        if activar:
            accion='1'
        else:
            accion='0'
        cursor = cls.db.cursor()
        cursor.execute(sql,(accion)) 
        cls.db.commit()
        '''
    @classmethod
    def act(cls,titulo, descripcion,mail_contacto, elementos_por_pagina):
        adm = AdministracionOrquesta.query.filter_by(id='1').first()
        adm.titulo = titulo
        adm.descripcion = descripcion
        adm.mail_contacto = mail_contacto
        adm.elementos_por_pagina = elementos_por_pagina
        db.session.commit()
        '''
        sql = """
            UPDATE administracion_orquesta AS a
            SET a.titulo = %s , a.descripcion = %s , a.mail_contacto = %s , a.elementos_por_pagina = %s 
            WHERE a.id = 1
        """        
        cursor = cls.db.cursor()
        cursor.execute(sql, (titulo, descripcion, mail_contacto, elementos_por_pagina))
        cls.db.commit() 
        '''