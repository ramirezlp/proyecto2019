from flask import redirect, render_template, request, url_for, session, abort, flash, jsonify
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.models.usuario_tiiene_rol import Usuario_tiene_rol
from flaskps.models.rol import Rol
from flaskps.helpers.auth import authenticated, admin
from flaskps.helpers.decorators import esta_en_mantenimiento, tiene_permiso, is_authenticated
from flaskps.models.administracion_orquesta import AdministracionOrquesta
import json
from flaskps.resources import auth
from werkzeug.security import generate_password_hash, check_password_hash

@esta_en_mantenimiento
def home():
    administracion = AdministracionOrquesta.query.filter_by(id='1').first()
    return render_template('home2.html', administracion=administracion)        

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('usuario_show', 'usuario_index')
def index():
    User.db = get_db()
    users = User.all()
    

    return render_template('user/index2.html', users=users, administracion=AdministracionOrquesta.query.filter_by(id='1').first())

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('usuario_new')
def new():
    #debe retornar la vista para registrar un nuevo docente/preceptor. Quiza deberia estar en el controlador del admin
    return render_template('user/new2.html', administracion=AdministracionOrquesta.query.filter_by(id='1').first())

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('usuario_new')
def create():
    #esta mal imlementado esto ? ya no esta el metodo index para esto ?

    User.db = get_db()
    r = request.form
    if User.existing_username(request.form["username"]):
        flash("ese nombre de usuario ya se encuentra utilizado", "warning")
    else:
        User.create(r["email"], generate_password_hash(r["password"]), r["firstname"], r["lastname"], r["username"])
    return redirect(url_for('user_index'))

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('usuario_show', 'usuario_index')
def search():
    User.db = get_db()
    print(request.args.get("activo-inactivo"))
    print(request.args.get("search_user"))
    if int(request.args.get("activo-inactivo")) != 2:
        users = User.find_by_name_and_active(request.args.get("search_user"), request.args.get("activo-inactivo"))
    else:
        print("entreeeee")
        users = User.find_by_name(request.args.get("search_user"))
        print(users)
    AdministracionOrquesta.db = get_db()
    administracion = AdministracionOrquesta.query.filter_by(id=1).first()
    return render_template("user/index2.html", users=users, msg="Resultados de Busqueda",administracion=administracion)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('configuracion_update')
def configure():
    if request.method == "POST":
        r=request.form
        AdministracionOrquesta.act(r['titulo'],r['descripcion'],r['mail_contacto'],r['elementos_por_pagina'])
        return redirect(url_for('configuracion'))
    else:
        administracion = AdministracionOrquesta.query.filter_by(id='1').first()
        return render_template("/user/config_template.html",administracion=administracion)


@is_authenticated
@esta_en_mantenimiento
@tiene_permiso('usuario_update')
def edit_form():
    User.db = get_db()
    Usuario_tiene_rol.db = get_db()
    Rol.db = get_db()
    user = User.find_by_id(request.form["id"])
    rolesId = Usuario_tiene_rol.find_by_user(user.id)
    rol_ids = [rol.rol_id for rol in rolesId]
    roles_del_usuario = [rol.nombre for rol in (Rol.find_by_rol_ids(rol_ids))]
    todos_los_roles = [(rol.id, rol.nombre) for rol in Rol.all()]
    roles = {}
    roles['usuario'] = roles_del_usuario
    roles['totales'] = todos_los_roles    
    AdministracionOrquesta.db = get_db()
    administracion = AdministracionOrquesta.query.filter_by(id=1).first()
    return render_template("/user/test-edicion-usuario.html", roles=roles, id=request.form["id"], user=user,administracion=administracion)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('usuario_update')
def edit():    
    if not authenticated or not admin:
        abort(401)

    roles_usuario= set(int(rol_id) for rol_id in request.get_json()["roles"])
    roles_no_tiene = set(int(rol.id) for rol in Rol.all())
    roles_no_tiene = roles_no_tiene - roles_usuario

    r = request.get_json()["form"]
    User.db = get_db()
    User.act(r["id"], r["email"], r["contraseña"], r["estado"], r["nombre"], r["apellido"], r["username"])
    Usuario_tiene_rol.db = get_db()
    for rol in roles_usuario:
        Usuario_tiene_rol.insertar_rol(r['id'], rol)
    for rol in roles_no_tiene:
        Usuario_tiene_rol.delete_rol_usuario(r['id'], rol)

    return jsonify(activado=True)   

def activo_desactivo_sitio():
    if not authenticated or not admin:
        abort(401) 
    if int(request.get_json()['activar']) == 1:
        AdministracionOrquesta.db = get_db()
        AdministracionOrquesta.activar_desactivar_sitio(False)
        return jsonify(activado=True)
    else:
        AdministracionOrquesta.db = get_db()
        AdministracionOrquesta.activar_desactivar_sitio(True)
        return jsonify(activado=False)

def state_toggle():    
    if not authenticated or not admin:
        abort(401)
    User.db=get_db()
    user=User.find_by_id(request.get_json()['id'])
    if user.email == session.get("user"):
        return jsonify(activado=False)
    User.change_state(request.get_json()['id'])
    return jsonify(activado=True)   

def check_username():
    if not authenticated or not admin:
        abort(401)
    User.db = get_db()
    # print(request.get_json()['username'])
    user = User.existing_username(request.get_json()['username'])
    if not user:
        return jsonify(estado="nuevo")
    else:
        try: # adaptacion para que se pueda seleccionar el mismo id en el editar_usuario
            if user["id"] == int(request.get_json()["id"]):
                return jsonify(estado="nuevo")
            else:
                return jsonify(estado="usado")
        except:
            return jsonify(estado="usado")

def check_email():
    if not authenticated or not admin:
        abort(401)
    User.db = get_db()
    user = User.find_by_email(request.get_json()['email'])
    if not user:
        return jsonify(estado="nuevo")
        
    else:
        try: # adaptacion para que se pueda seleccionar el mismo email en el editar_usuario
            if user.id == int(request.get_json()["id"]):
                return jsonify(estado="nuevo")
            else:
                return jsonify(estado="usado")
        except:
            return jsonify(estado="usado")
            
@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('usuario_destroy')
def user_delete():
    if not authenticated or not admin:
        abort(401)
    User.db=get_db()
    user=User.find_by_id(request.get_json()['id'])
    if user.email == session.get("user"):
        return jsonify(activado=False)
    User.delete(request.get_json()['id'])   
    return jsonify(activado=True)   
        

