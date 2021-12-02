from flask import redirect, render_template, request, url_for, abort, session, flash
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.models.rol import Rol
from flaskps.models.usuario_tiiene_rol import Usuario_tiene_rol 
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.models.rol_tiene_permiso import Rol_tiene_permiso
from flaskps.models.permiso import Permiso
from flaskps.resources import __init__ as init
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import logout_user, current_user, LoginManager
from flask_login import login_required, login_user


def login():
    #print("eeeee")
    if request.method == 'POST':
        return authenticate(request.form)
    else:
        return render_template('auth/login_template.html', administracion=AdministracionOrquesta.query.filter_by(id=1))


def authenticate(params):

    User.db = get_db()
    user = User.find_by_email(params['email'])
    if user:
        if check_password_hash(user.password, params["password"]):
            if not user.activo:
                flash("El usuario se encuentra inactivo","danger")
                return redirect(url_for('auth_login')) 
            session['user'] = user.email
            login_user(user)
            flash("La sesión se inició correctamente.", "success")
            return redirect(url_for('home'))
        else:
            flash("Usuario o clave incorrecto.","warning")    
    else:
        flash("Usuario o clave incorrecto.","warning")
    return redirect(url_for('auth_login'))    
        #print(url_for('home'))
        #print(redirect(url_for('auth_login')))


    # COMENTADO PRA PODER PROBAR SI ANDA BIEN EL MODELO DE USERS SACAR COMENTARIO DESPUES
    # if not has_rol(user['email'],['administrador']):
    #     AdministracionOrquesta.db= get_db()
    #     administracion=AdministracionOrquesta.get() 
    #     if not administracion['sitio_activo']:
    #         flash("El sitio se encuentra en mantenimiento","danger")
    #         return redirect(url_for('auth_login'))
    

def logout():
    del session['user']
    session.clear()
    logout_user()
    return redirect(url_for('home'))

def is_admin(email, adm="Administrador"):
    User.db = get_db()
    Rol.db = get_db()
    Usuario_tiene_rol.db = get_db()
    if email:
        user = User.find_by_email(email)
    else:
        user=None        
    rol = Rol.find_by_rol_name(adm)        
    if user and rol:
        if Usuario_tiene_rol.find_by_user_and_rol(user.id, rol.id):
            return True
    return False

def has_permisions(email, permisos):
    print('permisos a buscar: ', permisos)
    User.db = get_db()
    Rol.db = get_db()
    Usuario_tiene_rol.db = get_db()
    Rol_tiene_permiso.db = get_db()
    Permiso.db = get_db()
    user=None
    print(email)
    if email:
        user = User.find_by_email(email)
    if user:
        permisos_ids = []
        for permiso in permisos:
            permisos_ids.append(Permiso.find_by_nombre(permiso).id)
        print("id de permisos necesarios: ", permisos_ids)
        roles_del_usuario = [rol.rol_id for rol in Usuario_tiene_rol.find_by_user(user.id)]
        print("roles del usuario: ", roles_del_usuario)
        for id_rol in roles_del_usuario:
            if len(permisos_ids) > 0:
                permisos_de_este_rol = Rol_tiene_permiso.find_permisos_by_rolId(id_rol)
                print("permisos de este rol: ", permisos_de_este_rol)
                for per in permisos_de_este_rol:
                    if per in permisos_ids:
                        permisos_ids.remove(per)
        print("permisos que les faltan al usuario para acceder: ", permisos_ids)
        if len(permisos_ids) == 0:
            return True
    return False
    
            
        #     if r and not Usuario_tiene_rol.find_by_user_and_rol(user.id, r.id):
        #         return False
        # return True
    return False
        
