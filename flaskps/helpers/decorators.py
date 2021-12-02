from flask import render_template, request, url_for, session, abort
from flaskps.db import get_db
from flaskps.helpers.auth import authenticated
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.models.user import User
from functools import wraps
from flaskps.resources import auth



#VALIDA SI EL USUARIO SE ENCUENTRA AUTENTICADO. SE INVOCA ASI: @is_authenticated
def is_authenticated(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not authenticated(session):
            abort(401)
        else:
            User.db=get_db()
            user= User.query.filter_by(email=session.get("user")).first()
            if not user.activo:
                auth.logout()
                abort(409)
        return f(*args, **kwargs)
    return wrap

#VALIDA SI UN USUARIO TIENE PERMISOS.
#LOS PERMISOS SE ENVIAN COMO PARAMETROS. EJEMPLO: @tiene_permiso('profesor','administrador')
#                                                 @tiene_permiso('administrador')
def tiene_permiso(*permisos):
    def wrapper(func):
        def inner(*args, **kwargs):
            if not auth.has_permisions(session.get("user"), permisos):
                abort(401)
            return func(*args, **kwargs)
        return inner
    return wrapper

#VALIDA SI EL SITIO ESTA EN MANTENIMIENDO. SE DEBE INVOCAR ASI: @esta_en_mantenimiento
def esta_en_mantenimiento(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not auth.has_permisions(session.get("user"),['configuracion_update']):
            administracion=AdministracionOrquesta.query.filter_by(id='1').first()
            print('administracion: ',AdministracionOrquesta.query.filter_by(id='1').all())
            print('administracion activo: ',AdministracionOrquesta.query.filter_by(id='1').first().sitio_activo)
            if not int(administracion.sitio_activo):
                kwargs = {"error_name": "Sitio en mantenimiento.",
                        "error_description": "Vuelva mas tarde."
                        }
                return render_template('mantenimiento.html', **kwargs)
        return f(*args, **kwargs)
    return wrap