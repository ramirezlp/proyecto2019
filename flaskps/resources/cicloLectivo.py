from flask import redirect, render_template, request, url_for, session, abort, flash, jsonify
from flaskps.models import cicloLectivo
from flaskps.models.taller import Taller
from flaskps.models.cicloLectivoTaller import CicloLectivoTaller
from flaskps.models.user import User
from flaskps.models.docenteResponsableTaller import DocenteResponsableTaller
from flaskps.models.estudianteCicloLectivoTaller import EstudianteCicloLectivoTaller
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.db import get_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey
from flaskps.helpers.decorators import esta_en_mantenimiento, tiene_permiso, is_authenticated
import datetime

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_index','administracion_show') 
def index():
	#dame todos los ciclos y pasalos a la vista
	cicloLectivo.db = get_db()
	ciclos = cicloLectivo.CicloLectivo.all()
	Taller.db = get_db()
	talleres = Taller.query.all()
	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
	print(talleres)
	return render_template('ciclos_lectivos/ciclos_lectivos_index.html', ciclos=ciclos, administracion=administracion, talleres=talleres)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_index','administracion_show')
def ver_talleres():
	#dame los talleres asociados a ese cilo lectivo.
	#pasalos a la vista
	r = request.args
	ciclo = cicloLectivo.CicloLectivo.find_by_id(r["id"])
	administracion = AdministracionOrquesta.query.filter_by(id='1').first()	
	rels = CicloLectivoTaller.find_by_ciclo_lectivo_id(r["id"])
	talleres = []
	for rel in rels:
		talleres.append(Taller.find_by_id(rel.taller_id))
	return render_template("ciclos_lectivos/ver_talleres.html",administracion=administracion,talleres=talleres,ciclo=ciclo)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_destroy')
def desasignar_taller():	
	r = request.form	
	ciclo_taller = CicloLectivoTaller.find_by_taller_id_and_ciclo_id(r["taller_id"],r["ciclo_id"])
	docentes = DocenteResponsableTaller.find_by_ciclo_lectivo_taller_id(ciclo_taller.id)
	estudiantes = EstudianteCicloLectivoTaller.find_by_ciclo_lectivo_taller_id(ciclo_taller.id)
	if estudiantes or docentes:
		flash("no se puede desasignar el ciclo del taller ya que este posee docentes y/o estudiantes asociados","warning")	
	else:
		CicloLectivoTaller.db = get_db()
		CicloLectivoTaller.delete(ciclo_taller.id)
		flash("se desasigno el ciclo lectivo del taller con exito","success")
	#ver si hay docentes asociados al ciclo taller
	#ver si hay alumnos asociados al ciclo taller 
	#si no se cumple nada de lo anteriro borrar la relacion

	return redirect(url_for("ciclos"))

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_update')
def edit():
	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
	if request.method == "POST":
		cicloLectivo.CicloLectivo.db = get_db()
		ciclos = cicloLectivo.CicloLectivo.all()
		r = request.form		
		cicloLectivo.CicloLectivo.update(r["id"],r["fecha_ini"],r["fecha_fin"],r["semestre"])	
		flash("Edicion exitosa","success")
		return redirect(url_for("ciclos"))
	else:
		ciclo = cicloLectivo.CicloLectivo.find_by_id(request.args["id"])
		fecha_ini = ciclo.fecha_ini.strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]
		fecha_fin = ciclo.fecha_fin.strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]		
		return render_template('ciclos_lectivos/ciclo_lectivo_edit.html',administracion=administracion,ciclo=ciclo,fecha_ini=fecha_ini,fecha_fin=fecha_fin)	

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new',)
def new():	
	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
	return render_template('ciclos_lectivos/ciclo_lectivo_new.html',administracion=administracion)	

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new',)
def create():
	cicloLectivo.CicloLectivo.db = get_db()
	ciclos = cicloLectivo.CicloLectivo.all()
	r = request.form			
	f_ini = datetime.datetime.strptime(r["fecha_ini"],"%Y-%m-%d")
	f_fin = datetime.datetime.strptime(r["fecha_fin"],"%Y-%m-%d")
	f_actual = datetime.datetime.now().strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]
	f_actual = datetime.datetime.strptime(f_actual,"%Y-%m-%d")
	#if (not (f_actual <= f_ini) and (f_actual < f_fin)):
	#	flash("las fechas ingresadas son invalidas","warning")
	#	return redirect(url_for("ciclo_new"))
	#else:
	if(not f_fin > f_ini):
		flash("La fecha de fin debe ser mayor a la de inicio de semestre","warning")
		return redirect(url_for("ciclo_new"))
	else:
		if(r["semestre"]=="1"):
			if(f_ini.month != 1 or f_fin.month > 5):					
				flash("No se creo el ciclo lectivo, motivo: El semestre ingresado no es coherente con la fecha de inicio","warning")
				return redirect(url_for('ciclo_new'))				
		else:
			if(f_ini.month < 6 or f_fin.year > f_ini.year):
				flash("No se creo el ciclo lectivo, motivo: El semestre ingresado no es coherente con la fecha de inicio","warning")
				return redirect(url_for('ciclo_new'))					
		cicloLectivo.CicloLectivo.create(r["fecha_ini"],r["fecha_fin"],r["semestre"])
		administracion = AdministracionOrquesta.query.filter_by(id='1').first()
		flash("Has creado un nuevo ciclo lectivo","success")
		return redirect(url_for("ciclos"))

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_destroy',)
def delete():
	r = request.form	
	cicloLectivo.CicloLectivo.db = get_db()
	if CicloLectivoTaller.find_by_ciclo_lectivo_id(r["id"]):
		flash("no se pudo eleminar el ciclo, este se encuentra asociado a uno o mas talleres","warning")
		return redirect(url_for("ciclos"))
	cicloLectivo.CicloLectivo.delete(r["id"])
	flash("Se ha excluido el ciclo lectivo","success")
	return redirect(url_for("ciclos"))

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new',)
def asignar_taller_a_ciclo():
	r = request.form
	print(r["taller"])
	print(r["ciclo_lectivo"])		
	CicloLectivoTaller.db = get_db()
	aux = CicloLectivoTaller.query.filter_by(taller_id=r["taller"], ciclo_lectivo_id=r["ciclo_lectivo"]).first()
	if aux:
		flash("ese taller ya se encuentra asignado a ese ciclo lectivo", "warning")
	else:
		CicloLectivoTaller.create(r["taller"], r["ciclo_lectivo"])
		flash("se asigno correctamente", "success")
	return redirect(url_for('ciclos'))