from flask import redirect, render_template, request, url_for, session, abort, flash, jsonify
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.models.usuario_tiiene_rol import Usuario_tiene_rol
from flaskps.models.rol import Rol
from flaskps.helpers.auth import authenticated, admin
from flaskps.helpers.decorators import esta_en_mantenimiento, tiene_permiso, is_authenticated
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.models.estudiante import Barrio, Estudiante, Escuela, Responsable, ResponsableEstudiante, Genero, Nivel
from flaskps.models.estudianteCicloLectivoTaller import EstudianteCicloLectivoTaller
from flaskps.models.cicloLectivoTaller import CicloLectivoTaller
from flaskps.models.cicloLectivo import CicloLectivo
import json
from flaskps.resources import auth
import requests
import datetime
from sqlalchemy.orm import raiseload

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('estudiante_show', 'estudiante_new', 'estudiante_index', 'estudiante_destroy', 'estudiante_update')
def crud_estudiantes():
    estudiantes = Estudiante.query.all()
    generos = Genero.query.all()
    barrios = Barrio.query.order_by(Barrio.nombre).all()
    escuelas = Escuela.query.all()
    niveles = Nivel.query.all()
    administracion = AdministracionOrquesta.query.filter_by(id='1').first()
    localidades=requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad").json()
    tipos_doc=requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento").json()

    return render_template('crud_estudiantes.html', estudiantes=estudiantes,administracion=administracion,
    localidades=localidades,tipos_doc=tipos_doc,escuelas=escuelas,niveles=niveles,barrios=barrios,generos=generos)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('estudiante_new')
def crear_estudiantes():
    db = get_db()
    r = request.form
    if not request.form:
        flash("No pudo guardarse el estudiante", "warning")
    else:
        if not (r['nombre'] and r['apellido'] and r['fecha_nacimiento'] 
        and r['localidad'] and r['domicilio'] and r['genero'] and r['barrio'] 
        and r['tipo_doc'] and r['documento'] and r['escuela'] and r['nivel'] 
        and r['responsable'] and r['numero_contacto'] and r['email_contacto']):
            flash('No pudo guardarse el estudiante. Faltan campos','warning')
            return redirect(url_for('estudiantes'))

        if any(char.isdigit() for char in r['nombre']+r['apellido']):
            flash('No pudo guardarse el estudiante. Nombre no válido','warning')
            return redirect(url_for('estudiantes'))
        try:
            text=datetime.datetime.strptime(r['fecha_nacimiento'],'%Y-%m-%d').date()
            if str(text.year) < '1930' or str(text.year) > str(datetime.datetime.now().year):
                flash('No pudo guardarse el estudiante. Fecha de nacimiento no valida','warning')
                return redirect(url_for('estudiantes')) 
        except:
            flash('No pudo guardarse el estudiante. Fecha de nacimiento no valida','warning')
            return redirect(url_for('estudiantes'))
        if any(char.isdigit() for char in r['lugar_nacimiento']):
            flash('No pudo guardarse el estudiante. Lugar de nacimiento no válido','warning')
            return redirect(url_for('estudiantes'))
        try:
            text=int(r['localidad'])
        except:
            flash('No pudo guardarse el estudiante. Localidad no valida','warning')
            return redirect(url_for('estudiantes'))
        try:
            text=int(r['genero'])
        except:
            flash('No pudo guardarse el estudiante. Genero no valido','warning')
            return redirect(url_for('estudiantes'))  
        try:
            text=int(r['barrio'])
        except:
            flash('No pudo guardarse el estudiante. Barrio no valido','warning')
            return redirect(url_for('estudiantes'))   
        try:
            tipo=int(r['tipo_doc'])
            dni=int(r['documento'])
            if dni > 99999999 or dni < 1000000:
                flash('No pudo guardarse el estudiante. Documento no valido','warning')
                return redirect(url_for('estudiantes'))  
        except:
            flash('No pudo guardarse el estudiante. Documento no valido','warning')
            return redirect(url_for('estudiantes'))     
        if(r['telefono']):
            try:
                telefono=int(r['telefono'])
                if telefono < 100000 or telefono > 1000000000000:
                    flash('No pudo guardarse el estudiante. Telefonos no validos','warning')
                    return redirect(url_for('estudiantes'))  
            except:
                flash('No pudo guardarse el estudiante. Telefonos no validos','warning')
                return redirect(url_for('estudiantes'))  
        try:
            telefono2=int(r['numero_contacto'])
            if telefono2 < 100000 or telefono2 > 1000000000000:
                flash('No pudo guardarse el estudiante. Numero de contacto','warning')
                return redirect(url_for('estudiantes'))  
        except:
            flash('No pudo guardarse el estudiante. Numero de contacto','warning')
            return redirect(url_for('estudiantes'))   
        try:
            text=int(r['nivel'])
        except:
            flash('No pudo guardarse el estudiante. Nivel no valido','warning')
            return redirect(url_for('estudiantes'))                   
        try:
            text=int(r['escuela'])
        except:
            flash('No pudo guardarse el estudiante. Escuela no valida','warning')
            return redirect(url_for('estudiantes'))   
        if any(char.isdigit() for char in r['responsable']):
            flash('No pudo guardarse el estudiante. Responsable no válido','warning')
            return redirect(url_for('estudiantes'))
        if r['email_contacto'].find('@') == -1:
            flash('No pudo guardarse el estudiante. Email no válido','warning')
            return redirect(url_for('estudiantes')) 
        estudiante = Estudiante(nombre=r['nombre'],apellido=r['apellido'],fecha_nacimiento=r['fecha_nacimiento'],
        lugar_de_nacimiento=r['lugar_nacimiento'],localidad_id=r['localidad'],domicilio=r['domicilio'],
        genero_id=r['genero'],barrio_id=r['barrio'],tipo_doc_id=r['tipo_doc'],documento=r['documento'],
        telefono=r['telefono'],escuela_id=r['escuela'],nivel_id=r['nivel'],responsable=r['responsable'], numero_contacto=r['numero_contacto'], email_contacto=r['email_contacto'])
        db.session.add(estudiante)
        db.session.commit()
        flash("Se agrego correctamente al estudiante", "success")
    return redirect(url_for('estudiantes'))


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('estudiante_destroy')
def eliminar_estudiante():
    db = get_db()
    for r in EstudianteCicloLectivoTaller.query.filter_by(estudiante_id = request.get_json()['id'].split("-")[1]).all():
        for clt in CicloLectivoTaller.query.filter_by(id=r.ciclo_lectivo_taller_id).all():
            for cl in CicloLectivo.query.filter_by(id=clt.ciclo_lectivo_id).all():
                if int(cl.fecha_fin.year) == int(datetime.datetime.now().year):
                    flash("No se pudo eliminar el estudiante, ya que se encuentra asignado a uno o mas talleres de este año","warning")
                    return jsonify(deleted=False)   
    EstudianteCicloLectivoTaller.query.filter_by(estudiante_id=request.get_json()['id'][11:]).delete() 
    db.session.delete(Estudiante.query.filter_by(id=request.get_json()['id'][11:]).first())
    db.session.commit()
    return jsonify(deleted=True)


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('estudiante_index', 'estudiante_show')
def detalle_estudiante():
    db = get_db()
    estudiante = Estudiante.query.filter_by(id=request.get_json()['id'][11:]).first()
    fecha = estudiante.fecha_nacimiento.strftime('%Y-%m-%d')
    localidad=requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad/"+str(estudiante.localidad_id)).json()
    tipo_doc=requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento/"+str(estudiante.tipo_doc_id)).json()
    return jsonify(estudiante=estudiante.serialize(),localidad=localidad,tipo_doc=tipo_doc,fecha=fecha)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('estudiante_update')
def modificar_estudiante():
    db = get_db()
    r = dict(request.form)
    if not request.form:
        flash("No pudo guardarse el estudiante", "warning")
    else:
        try:
            if not (r['nombre_mod'] and r['apellido_mod'] and r['fecha_nacimiento_mod'] 
            and r['localidad_mod'] and r['domicilio_mod'] and r['genero_mod'] and r['barrio_mod'] 
            and r['tipo_doc_mod'] and r['documento_mod'] and r['escuela_mod'] and r['nivel_mod'] 
            and r['responsable_mod'] and r['numero_cont_mod'] and r['email_cont_mod']):
                flash('No pudo guardarse el estudiante. Faltan campos','warning')
                return redirect(url_for('estudiantes'))
        except:
            flash('No pudo guardarse el estudiante. Faltan campos','warning')
            return redirect(url_for('estudiantes'))

        if any(char.isdigit() for char in r['nombre_mod']+r['apellido_mod']):
            flash('No pudo guardarse el estudiante. Nombre no válido','warning')
            return redirect(url_for('estudiantes'))
        try:
            text=datetime.datetime.strptime(r['fecha_nacimiento_mod'],'%Y-%m-%d').date()
            if str(text.year) < '1930' or str(text.year) > str(datetime.datetime.now().year):
                flash('No pudo guardarse el estudiante. Fecha de nacimiento no valida','warning')
                return redirect(url_for('estudiantes')) 
        except:
            flash('No pudo guardarse el estudiante. Fecha de nacimiento no valida','warning')
            return redirect(url_for('estudiantes'))
        try:
            text=int(r['localidad_mod'])
        except:
            flash('No pudo guardarse el estudiante. Localidad no valida','warning')
            return redirect(url_for('estudiantes'))
        try:
            text=int(r['genero_mod'])
        except:
            flash('No pudo guardarse el estudiante. Genero no valido','warning')
            return redirect(url_for('estudiantes'))  
        try:
            text=int(r['barrio_mod'])
        except:
            flash('No pudo guardarse el estudiante. Barrio no valido','warning')
            return redirect(url_for('estudiantes'))   
        try:
            tipo=int(r['tipo_doc_mod'])
            dni=int(r['documento_mod'])
            if dni > 99999999 or dni < 1000000:
                flash('No pudo guardarse el estudiante. Documento no valido','warning')
                return redirect(url_for('estudiantes'))  
        except:
            flash('No pudo guardarse el estudiante. Documento no valido','warning')
            return redirect(url_for('estudiantes'))     
        if(r['telefono_mod']):
            try:
                telefono=int(r['telefono_mod'])
                if telefono < 100000 or telefono > 1000000000000:
                    flash('No pudo guardarse el estudiante. Telefonos no validos','warning')
                    return redirect(url_for('estudiantes'))  
            except:
                flash('No pudo guardarse el estudiante. Telefonos no validos','warning')
                return redirect(url_for('estudiantes'))              
        try:
            telefono2=int(r['numero_cont_mod'])
            if telefono2 < 100000 or telefono2 > 1000000000000:
                flash('No pudo guardarse el estudiante. Numero de contacto no valido','warning')
                return redirect(url_for('estudiantes'))  
        except:
            flash('No pudo guardarse el estudiante. Numero de contacto','warning')
            return redirect(url_for('estudiantes'))
        try:
            text=int(r['nivel_mod'])
        except:
            flash('No pudo guardarse el estudiante. Nivel no valido','warning')
            return redirect(url_for('estudiantes'))                   
        try:
            text=int(r['escuela_mod'])
        except:
            flash('No pudo guardarse el estudiante. Escuela no valida','warning')
            return redirect(url_for('estudiantes'))   
        if any(char.isdigit() for char in r['responsable_mod']):
            flash('No pudo guardarse el estudiante. Responsable no válido','warning')
            return redirect(url_for('estudiantes'))
        if r['email_cont_mod'].find('@') == -1:
            flash('No pudo guardarse el estudiante. Email no válido','warning')
            return redirect(url_for('estudiantes')) 
        estudiante = Estudiante.query.filter_by(id=r['id_mod']).update(dict(nombre=r['nombre_mod'],apellido=r['apellido_mod'],fecha_nacimiento=r['fecha_nacimiento_mod'],
        lugar_de_nacimiento=r['lugar_nacimiento_mod'],localidad_id=r['localidad_mod'],domicilio=r['domicilio_mod'],
        genero_id=r['genero_mod'],barrio_id=r['barrio_mod'],tipo_doc_id=r['tipo_doc_mod'],documento=r['documento_mod'],
        telefono=r['telefono_mod'],escuela_id=r['escuela_mod'],nivel_id=r['nivel_mod'],responsable=r['responsable_mod'], numero_contacto=r['numero_cont_mod'], email_contacto=r['email_cont_mod']))
        db.session.commit()
        flash("Se modifico correctamente el estudiante","success")


    return redirect(url_for('estudiantes'))


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('estudiante_show', 'estudiante_index')
def documento_estudiante():
    #TODO
    print(request.get_json())
    estudiantes= Estudiante.query.filter_by(tipo_doc_id=request.get_json()['tipo_doc'],documento= request.get_json()['documento'])
    estudiantes_all= estudiantes.all()
    if not request.get_json()['id']:
        print('aaaa ')
        ok = False if estudiantes_all else True 
    else:
        if estudiantes_all and int(estudiantes.first().id) == int(request.get_json()['id']):
            ok = True
        elif estudiantes_all and int(estudiantes.first().id) != int(request.get_json()['id']) :
            ok = False
        else:
            ok = True
    return jsonify(ok=ok)

