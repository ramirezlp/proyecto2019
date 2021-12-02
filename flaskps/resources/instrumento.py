from flask import redirect, render_template, request, url_for, session, abort, flash, jsonify
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.models.usuario_tiiene_rol import Usuario_tiene_rol
from flaskps.models.rol import Rol
from flaskps.helpers.auth import authenticated, admin
from flaskps.helpers.decorators import esta_en_mantenimiento, tiene_permiso, is_authenticated
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.models.estudiante import Barrio, Estudiante, Escuela, Responsable, ResponsableEstudiante, Genero, Nivel
from flaskps.models.instrumento import TipoInstrumento, Instrumento
from flaskps.models.estudianteCicloLectivoTaller import EstudianteCicloLectivoTaller
from flaskps.models.cicloLectivoTaller import CicloLectivoTaller
from flaskps.models.cicloLectivo import CicloLectivo
import json
from flaskps.resources import auth
import requests
import datetime
from sqlalchemy.orm import raiseload
from werkzeug import secure_filename
import os
from flaskps.const import UPLOAD_FOLDER, FORMATOS_DE_IMAGEN

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_index', 'docente_show')
def crud_instrumento():
    instrumentos = Instrumento.query.all()
    tipo_instrumentos = TipoInstrumento.query.all()
    administracion = AdministracionOrquesta.query.filter_by(id='1').first()
    return render_template('instrumentos/crud_instrumentos.html', instrumentos=instrumentos,path=UPLOAD_FOLDER+'/', tipo_instrumentos=tipo_instrumentos, administracion=administracion)


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_index', 'docente_show')
def detalle_instrumento():
    db = get_db()
    instrumento = Instrumento.query.filter_by(numero_inventario=request.get_json()['id'][12:]).first()
    return jsonify(instrumento=instrumento.serialize())

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new', 'administracion_destroy', 'administracion_update')
def eliminar_instrumento():
    db = get_db()
    db.session.delete(Instrumento.query.filter_by(numero_inventario=request.get_json()['numero_inventario'][12:]).first())
    db.session.commit()
    return jsonify(deleted=True)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new', 'administracion_destroy', 'administracion_update')
def crear_instrumento():
    db = get_db()
    r = request.form
    filename=None
    if not request.form:
        flash("No pudo guardarse el instrumento", "warning")
    else:
        if request.files['archivo']:
            f = request.files['archivo']
            filename = secure_filename(f.filename)
            if filename.find('.'):
                if filename.split('.')[1].lower() in FORMATOS_DE_IMAGEN:
                    f.save(UPLOAD_FOLDER + '/' +filename)
                else:
                    flash('No pudo guardarse el instrumento. Formato de imagen no permitido','warning')
                    return redirect(url_for('instrumentos'))
        if not (r['nombre'] and r['numero_inventario_nuevo'] and r['tipo_instrumento']):
            flash('No pudo guardarse el instrumento. Faltan campos','warning')
            return redirect(url_for('instrumentos'))
        if len(str(r['nombre'])) > 30:
            flash('No pudo guardarse el instrumento. Numero de inventario invalido','warning')
            return redirect(url_for('instrumentos')) 
        try:
            text=int(r['tipo_instrumento'])
        except:
            flash('No pudo guardarse el instrumento. Tipo de instrumento no valido','warning')
            return redirect(url_for('estudiantes'))
        instrumento = Instrumento(nombre=r['nombre'],numero_inventario=r['numero_inventario_nuevo'].upper(), tipo_instrumento_id=r['tipo_instrumento'],imagen=filename)
        db.session.add(instrumento)
        db.session.commit()
        flash("Se agrego correctamente el instrumento", "success")
    return redirect(url_for('instrumentos'))


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new', 'administracion_destroy', 'administracion_update')
def modificar_instrumento():
    db = get_db()
    r = request.form
    filename = Instrumento.query.filter_by(numero_inventario=r['numero_inventario_mod']).first().imagen
    if not request.form:
        flash("No pudo modificarse el instrumento", "warning")
    else:
        if request.files['archivo']:
            f = request.files['archivo']
            filename = secure_filename(f.filename)
            if filename.find('.'):
                if filename.split('.')[1].lower() in FORMATOS_DE_IMAGEN:
                    f.save(UPLOAD_FOLDER + '/' +filename)
                else:
                    flash('No pudo guardarse el instrumento. Formato de imagen no permitido','warning')
                    return redirect(url_for('instrumentos'))
        if not (r['nombre_mod'] and r['numero_inventario_nuevo_mod'] and r['tipo_instrumento_mod']):
            flash('No pudo modificarse el instrumento. Faltan campos','warning')
            return redirect(url_for('instrumentos'))
        if len(r['nombre_mod']) > 30:
            flash('No pudo modificarse el instrumento. Numero de inventario invalido','warning')
            return redirect(url_for('instrumentos'))    
        try:
            text=int(r['tipo_instrumento_mod'])
        except:
            flash('No pudo modificarse el instrumento. Tipo de instrumento no valido','warning')
            return redirect(url_for('estudiantes'))
        instrumento = Instrumento.query.filter_by(numero_inventario=r['numero_inventario_mod']).update(dict(nombre=r['nombre_mod']
        ,numero_inventario=r['numero_inventario_nuevo_mod'].upper(), tipo_instrumento_id=r['tipo_instrumento_mod'], imagen=filename))
        db.session.commit()
        flash("Se modifico correctamente el instrumento", "success")
    return redirect(url_for('instrumentos'))


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('estudiante_show', 'estudiante_index')
def numero_inventario_instrumento():
    #TODO
    instrumento= Instrumento.query.filter_by(numero_inventario=request.get_json()['numero_inventario_nuevo'].upper())
    instrumento_all= instrumento.all()
    if not request.get_json()['numero_inventario']:
        ok = False if instrumento_all else True 
    else:
        if instrumento_all and instrumento.first().numero_inventario == str(request.get_json()['numero_inventario']).upper():
            ok = True
        elif instrumento_all and instrumento.first().numero_inventario != str(request.get_json()['numero_inventario']).upper() :
            ok = False
        else:
            ok = True
    return jsonify(ok=ok)
