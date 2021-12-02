from flask import redirect, render_template, request, url_for, session, abort, flash, jsonify
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.models.usuario_tiiene_rol import Usuario_tiene_rol
from flaskps.models.rol import Rol
from flaskps.helpers.auth import authenticated, admin
from flaskps.helpers.decorators import esta_en_mantenimiento, tiene_permiso, is_authenticated
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.models.estudiante import Barrio, Estudiante, Escuela, Responsable, ResponsableEstudiante, Genero, Nivel
from flaskps.models.docente import Docente
from flaskps.models.docenteResponsableTaller import DocenteResponsableTaller
import json
import datetime
from flaskps.resources import auth
import requests
 
@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_new', 'docente_index', 'docente_show', 'docente_update', 'docente_destroy')
def crud_docentes():
    if request.method == "POST":
        r = request.form
        Docente.db = get_db()
        if not (r['nombre'] and r['apellido'] and r['fecha_nacimiento'] 
        and r['localidad'] and r['domicilio'] and r['genero']
        and r['tipo_doc'] and r['documento']):
            flash('No pudo guardarse el docente. Faltan campos','warning')
            return redirect(url_for('docentes'))

        if any(char.isdigit() for char in r['nombre']+r['apellido']):
            flash('No pudo guardarse el docente. Nombre no válido','warning')
            return redirect(url_for('docentes'))
        try:
            text=datetime.datetime.strptime(r['fecha_nacimiento'],'%Y-%m-%d').date()
            if str(text.year) < '1930' or str(text.year) > str(datetime.datetime.now().year):
                flash('No pudo guardarse el docente. Fecha de nacimiento no valida','warning')
                return redirect(url_for('docentes')) 
        except:
            flash('No pudo guardarse el docente. Fecha de nacimiento no valida','warning')
            return redirect(url_for('docentes'))
        # if any(char.isdigit() for char in r['domicilio']):
        #     flash('No pudo guardarse el docente. Lugar de nacimiento o domicilio no válido','warning')
        #     return redirect(url_for('docentes'))
        try:
            text=int(r['localidad'])
        except:
            flash('No pudo guardarse el docente. Localidad no valida','warning')
            return redirect(url_for('docentes'))
        try:
            text=int(r['genero'])
        except:
            flash('No pudo guardarse el docente. Genero no valido','warning')
            return redirect(url_for('docentes'))    
        try:
            tipo=int(r['tipo_doc'])
            dni=int(r['documento'])
            if dni > 99999999 or dni < 1000000:
                flash('No pudo guardarse el docente. Documento no valido','warning')
                return redirect(url_for('docentes'))  
        except:
            flash('No pudo guardarse el docente. Documento no valido','warning')
            return redirect(url_for('docentes'))     
        if(r['telefono']):
            try:
                telefono=int(r['telefono'])
                if telefono < 100000 or telefono > 1000000000000:
                    flash('No pudo guardarse el docente. Telefonos no validos','warning')
                    return redirect(url_for('docentes'))  
            except:
                flash('No pudo guardarse el docente. Telefonos no validos','warning')
                return redirect(url_for('docentes'))  
        docente = Docente(r["nombre"], r["apellido"], r["telefono"], r["fecha_nacimiento"], r["localidad"], r["domicilio"], r["genero"], r["tipo_doc"], r["documento"])
        Docente.db.session.add(docente)
        Docente.db.session.commit()
        flash("se agrego el docente correctamente", "success")
        return redirect(url_for('docentes'))
    else:
        docentes = Docente.query.all()
        generos = Genero.query.all()
        # barrios = Barrio.query.order_by(Barrio.nombre).all()
        administracion = AdministracionOrquesta.query.filter_by(id='1').first()
        localidades=requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad").json()
        tipos_doc=requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento").json()
        return render_template('crud_docentes.html', docentes=docentes,administracion=administracion, 
        localidades=localidades, tipos_doc=tipos_doc, generos=generos)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_index', 'docente_show')
def detalle_docente():
    db = get_db()
    print(request.get_json()['id'])
    docente = Docente.query.filter_by(id=request.get_json()['id']).first()
    fecha = docente.fecha_nac.strftime('%Y-%m-%d')
    localidad=requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad/"+str(docente.localidad_id)).json()
    tipo_doc=requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento/"+str(docente.tipo_doc_id)).json()
    return jsonify(docente=docente.serialize(), localidad=localidad, tipo_doc=tipo_doc, fecha=fecha)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_update')
def modificar_docente():
        db = get_db()
        r = request.form
        try:
            if not (r['nombre_mod'] and r['apellido_mod'] and r['fecha_nacimiento_mod'] 
            and r['localidad_mod'] and r['domicilio_mod'] and r['genero_mod']
            and r['tipo_doc_mod'] and r['documento_mod']):
                flash('No pudo guardarse el docente. Faltan campos','warning')
                return redirect(url_for('docentes'))
        except:
            flash('No pudo guardarse el docente. Faltan campos','warning')
            return redirect(url_for('docentes'))
        if any(char.isdigit() for char in r['nombre_mod']+r['apellido_mod']):
            flash('No pudo guardarse el docente. Nombre no válido','warning')
            return redirect(url_for('docentes'))
        try:
            text=datetime.datetime.strptime(r['fecha_nacimiento_mod'],'%Y-%m-%d').date()
            if str(text.year) < '1930' or str(text.year) > str(datetime.datetime.now().year):
                flash('No pudo guardarse el docente. Fecha de nacimiento no valida','warning')
                return redirect(url_for('docentes')) 
        except:
            flash('No pudo guardarse el docente. Fecha de nacimiento no valida','warning')
            return redirect(url_for('docentes'))
        # if any(char.isdigit() for char in r['domicilio_mod']):
        #     flash('No pudo guardarse el docente. Domicilio no válido','warning')
        #     return redirect(url_for('docentes'))
        try:
            print(int(r["localidad_mod"]))
            text=int(r['localidad_mod'])
        except:
            flash('No pudo guardarse el docente. Localidad no valida','warning')
            return redirect(url_for('docentes'))
        try:
            text=int(r['genero_mod'])
        except:
            flash('No pudo guardarse el docente. Genero no valido','warning')
            return redirect(url_for('docentes'))    
        try:
            tipo=int(r['tipo_doc_mod'])
            dni=int(r['documento_mod'])
            if dni > 99999999 or dni < 1000000:
                flash('No pudo guardarse el docente. Documento no valido','warning')
                return redirect(url_for('docentes'))  
        except:
            flash('No pudo guardarse el docente. Documento no valido','warning')
            return redirect(url_for('docentes'))     
        if(r['telefono_mod']):
            try:
                telefono=int(r['telefono_mod'])
                if telefono < 100000 or telefono > 1000000000000:
                    flash('No pudo guardarse el docente. Telefonos no validos','warning')
                    return redirect(url_for('docentes'))  
            except:
                flash('No pudo guardarse el docente. Telefonos no validos','warning')
                return redirect(url_for('docentes'))                          
        docente = Docente.query.filter_by(id=r['id_mod'])
        print(docente)
        docente.update(dict(nombre=r['nombre_mod'],apellido=r['apellido_mod'],fecha_nac=r['fecha_nacimiento_mod'],
        localidad_id=r['localidad_mod'], domicilio=r['domicilio_mod'], genero_id=r['genero_mod'], tipo_doc_id=r['tipo_doc_mod'], 
        numero_documento=r['documento_mod'], tel=r['telefono_mod']))
        db.session.commit()
        flash("Se modifico correctamente el docente","success")

        return redirect(url_for('docentes'))

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_destroy')
def eliminar_docente():
    if(DocenteResponsableTaller.find_by_docente_id(request.get_json()['id'])):
        flash("no se pudo eleminar el docente porque es responsable de uno o mas talleres","warning")        
        return jsonify(deleted=False)    
    db = get_db()
    db.session.delete(Docente.query.filter_by(id=request.get_json()['id']).first())
    db.session.commit()
    return jsonify(deleted=True)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_show')
def documento_docente():
    #TODO
    print(request.get_json())
    docentes= Docente.query.filter_by(tipo_doc_id=request.get_json()['tipo_doc'],numero_documento= request.get_json()['documento'])
    docentes_all= docentes.all()
    if not request.get_json()['id']:
        print('aaaa ')
        ok = False if docentes_all else True 
    else:
        if docentes_all and int(docentes.first().id) == int(request.get_json()['id']):
            ok = True
        elif docentes_all and int(docentes.first().id) != int(request.get_json()['id']) :
            ok = False
        else:
            ok = True
    return jsonify(ok=ok)