from flask import redirect, render_template, request, url_for, session, abort, flash, jsonify
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.models.usuario_tiiene_rol import Usuario_tiene_rol
from flaskps.models.rol import Rol
from flaskps.models.taller import Taller, Nucleo
from flaskps.models.cicloLectivoTaller import CicloLectivoTaller, Horario, CicloLectivoTallerHorario
from flaskps.models.cicloLectivo import CicloLectivo
from flaskps.models.docenteResponsableTaller import DocenteResponsableTaller
from flaskps.helpers.auth import authenticated, admin
from flaskps.helpers.decorators import esta_en_mantenimiento, tiene_permiso, is_authenticated
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.models.estudiante import Barrio, Estudiante, Escuela, Responsable, ResponsableEstudiante, Genero, Nivel
from flaskps.models.docente import Docente
from flaskps.models.estudianteCicloLectivoTaller import EstudianteCicloLectivoTaller
from flaskps.models.asistencias import AsistenciaTallerCicloLectivo
from flaskps.models.shared import db
from sqlalchemy import and_
import json
import datetime
from flaskps.resources import auth
import requests


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_show', 'administracion_index')
def index():
	Taller.db = get_db()
	talleres2 = Taller.query.all()
	talleres = []
	for taller in talleres2:
		lista_ciclos_validos  = []
		for ciclo_taller in CicloLectivoTaller.query.filter_by(taller_id=taller.id).all():
			if str(CicloLectivo.query.filter_by(id=ciclo_taller.ciclo_lectivo_id).first().fecha_fin) > str(datetime.datetime.now()):
				lista_ciclos_validos.append(ciclo_taller)
		talleres.append((taller,lista_ciclos_validos))
	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
	print(talleres)
	return render_template('talleres/talleres_index.html', administracion=administracion, talleres=talleres)


def manejarResponsables(ciclo_id,taller_id,docentes_ids):	
	DocenteResponsableTaller.db = get_db()	
	if(docentes_ids):					
		#consegui el id de la tupla taller_ciclo_lectivo que le coresponde a este taller y ciclo
		rel = CicloLectivoTaller.find_by_taller_id_and_ciclo_id(taller_id, ciclo_id)
		#consegui los docentes ya asociados a ese taller y ciclo(usando el id de arriba) *2
		responsables = DocenteResponsableTaller.find_by_ciclo_lectivo_taller_id(rel.id)
		responsables_ids =[]
		responsablesASacar = []			
		if(responsables):				
			for responsable in responsables:					
				responsables_ids.append(responsable.docente_id)
			for responsable_id in responsables_ids:										
				if (not str(responsable_id) in docentes_ids):						
					responsablesASacar.append(responsable_id)
				else:						
					docentes_ids.remove(str(responsable_id))						
		#si alguno de los docentes obtenidos en (2) no figura en entre los que vinieron en el requerimiento
			#borra la relacion de la tabla docente_responsable_taller
		#si alguno de los docentes del requerimiento no esta entre los obtenidos en (2)
			#agregalos a la tabla docente_responsable_taller			
		for d in docentes_ids:				
			DocenteResponsableTaller.create(d, rel.id)
		for r in responsablesASacar:
			Aborrar = DocenteResponsableTaller.find_by_docente_id_and_ciclo_lectivo_taller_id(r, rel.id)
			DocenteResponsableTaller.delete(Aborrar.id)		
	else:			
		rel = CicloLectivoTaller.find_by_taller_id_and_ciclo_id(taller_id, ciclo_id)
		DocenteResponsableTaller.eliminar_responsables_taller_ciclo(rel.id)		

def manejarEstudiantes(ciclo_id,taller_id,docentes_ids):	
	EstudianteCicloLectivoTaller.db = get_db()	
	if(docentes_ids):					
		#consegui el id de la tupla taller_ciclo_lectivo que le coresponde a este taller y ciclo
		rel = CicloLectivoTaller.find_by_taller_id_and_ciclo_id(taller_id, ciclo_id)
		#consegui los docentes ya asociados a ese taller y ciclo(usando el id de arriba) *2		
		responsables = EstudianteCicloLectivoTaller.find_by_ciclo_lectivo_taller_id(rel.id)
		responsables_ids =[]
		responsablesASacar = []			
		if(responsables):				
			for responsable in responsables:					
				responsables_ids.append(responsable.estudiante_id)
			for responsable_id in responsables_ids:										
				if (not str(responsable_id) in docentes_ids):						
					responsablesASacar.append(responsable_id)
				else:						
					docentes_ids.remove(str(responsable_id))						
		#si alguno de los docentes obtenidos en (2) no figura en entre los que vinieron en el requerimiento
			#borra la relacion de la tabla docente_responsable_taller
		#si alguno de los docentes del requerimiento no esta entre los obtenidos en (2)
			#agregalos a la tabla docente_responsable_taller			
		for d in docentes_ids:				
			EstudianteCicloLectivoTaller.create(d, rel.id)
		for r in responsablesASacar:
			Aborrar = EstudianteCicloLectivoTaller.find_by_estudiante_id_and_ciclo_lectivo_taller_id(r, rel.id)
			EstudianteCicloLectivoTaller.delete(Aborrar.id)		
	else:			
		rel = CicloLectivoTaller.find_by_taller_id_and_ciclo_id(taller_id, ciclo_id)
		EstudianteCicloLectivoTaller.eliminar_estudiantes_taller_ciclo(rel.id)		
		

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new', 'administracion_update','administracion_destroy')
def edit():	
	if(request.method == 'GET'):
		r = request.args		
		f_actual = datetime.datetime.now().strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]
		f_actual = datetime.datetime.strptime(f_actual,"%Y-%m-%d")
		rels = CicloLectivoTaller.find_by_taller_id(r["id"])#ciclos en q se dicto el taller	(idciclo/taller)	
		ciclos = []
		for rel in rels:
			c = CicloLectivo.find_by_id(rel.ciclo_lectivo_id)
			f_fin = c.fecha_fin.strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]
			f_fin = datetime.datetime.strptime(f_fin,"%Y-%m-%d")
			if(not f_actual > f_fin):
				ciclos.append(c)#ciclos en q se dicto el taller		
		ciclos_responsables = []
		for ciclo in ciclos:
			j = CicloLectivoTaller.find_by_taller_id_and_ciclo_id(r["id"], ciclo.id)
			resps = DocenteResponsableTaller.find_by_ciclo_lectivo_taller_id(j.id)
			algo = []
			for re in resps:
				algo.append(re.docente_id)
			tupla =  (ciclo.id ,algo)
			ciclos_responsables.append(tupla)			
		Taller.db = get_db()
		taller = Taller.find_by_id(r["id"])	
		administracion = AdministracionOrquesta.query.filter_by(id='1').first()
		docentes = Docente.all()	
		ciclos_responsables = json.dumps(ciclos_responsables)
		return render_template('talleres/taller_edit.html', administracion=administracion, taller=taller, ciclos=ciclos, docentes=docentes, ciclos_responsables= ciclos_responsables)	
	else:
		r = request.form
		taller_id = r["taller"]
		taller_nombre = r["nombre"]
		taller_nombre_corto = r["nombre_corto"]		
		ciclo_docentes = r["ciclos_docentes"]		
		ciclo_docentes = json.loads(ciclo_docentes)
		for c in ciclo_docentes:
			ciclo_id = c.pop(0)
			manejarResponsables(ciclo_id,taller_id,c)
		flash("Edicion exitosa","success")		
		return redirect(url_for('talleres'))

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new', 'administracion_update','administracion_destroy')
def asignarEstudiante():
	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
	if request.method == 'GET':
		r = request.args
		taller = Taller.find_by_id(r["taller_id"])
		TodosEstudiantes = Estudiante.query.all()
		#consegui los ciclos en que se dicto el taller
		ciclos = []
		for i in CicloLectivoTaller.find_by_taller_id(taller.id):		
			ciclos.append(CicloLectivo.find_by_id(i.ciclo_lectivo_id))
		#quedate con los que no hayan terminado
		f_actual = datetime.datetime.now().strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]
		f_actual = datetime.datetime.strptime(f_actual,"%Y-%m-%d")
		ciclosFinalizados = []
		for ciclo in ciclos:
			f_fin = ciclo.fecha_fin.strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]
			f_fin = datetime.datetime.strptime(f_fin,"%Y-%m-%d")
			if(f_actual >= f_fin):
				ciclosFinalizados.append(ciclo)
		for cicloFinalizado in ciclosFinalizados:
			ciclos.remove(cicloFinalizado)
		
		#saca los que no tengan docentes asignados
			#para cada ciclo consegui su relacion con el taller
				#si no existe un docente relacionado con esa relacion
					#saca el ciclo
		ciclosSinDocentes = []
		for ciclo in ciclos:			
			if(not DocenteResponsableTaller.find_by_ciclo_lectivo_taller_id(CicloLectivoTaller.find_by_taller_id_and_ciclo_id(taller.id, ciclo.id).id)):
				ciclosSinDocentes.append(ciclo)
		for cicloSinDocente in ciclosSinDocentes:
			ciclos.remove(cicloSinDocente)			

		
		#para los ciclos que no terminaron y q que tienen docentes, consegui sus estudiantes
		#crea el arreglo con el id de los ciclos, y el areglo de estudiantes de ese ciclo[(ciclo_id,[estudiantes]),((ciclo_id,[estudiantes])]						
		estudiantes_ciclos = []		
		for ciclo in ciclos:			
			estudiantes = []			
			if(EstudianteCicloLectivoTaller.find_by_ciclo_lectivo_taller_id(CicloLectivoTaller.find_by_taller_id_and_ciclo_id(taller.id,ciclo.id).id)):
				estudiantes = []
				for estudiante in (EstudianteCicloLectivoTaller.find_by_ciclo_lectivo_taller_id(CicloLectivoTaller.find_by_taller_id_and_ciclo_id(taller.id,ciclo.id).id)):
					estudiantes.append(estudiante.estudiante_id)
			tupla = (ciclo.id, estudiantes)
			estudiantes_ciclos.append(tupla)

		estudiantes_ciclos = json.dumps(estudiantes_ciclos)

		'''		
		ciclos_validos = []#ciclos en que se esta dictando el taller (id,inicio,fin,semsestre)
		ciclos_responsables = json.dumps(ciclos_responsables)
		'''
		return render_template("talleres/asignar_estudiantes.html",administracion=administracion,estudiantes=TodosEstudiantes, ciclos=ciclos, taller=taller, estudiantes_ciclos=estudiantes_ciclos)
	else:
		r = request.form
		taller_id = r["taller"]				
		ciclo_docentes = r["ciclos_docentes"]		
		ciclo_docentes = json.loads(ciclo_docentes)
		for c in ciclo_docentes:
			ciclo_id = c.pop(0)
			print("==========")
			print(ciclo_id)
			manejarEstudiantes(ciclo_id,taller_id,c)
		flash("Edicion exitosa","success")		
		return redirect(url_for('talleres'))
'''		r = request.form
		estudiante = r["estudiante_id"]
		ciclo_taller_id = r["ciclo_taller_id"]
		taller = r["taller"]
		CicloLectivoTaller.db = get_db()
		ciclo = CicloLectivoTaller.find_by_id(ciclo_taller)
		f_actual = datetime.datetime.now().strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]
		f_actual = datetime.datetime.strptime(f_actual,"%Y-%m-%d")
		f_fin = ciclo.fecha_fin.strftime("%Y-%m-%d (%H:%M:%S.%f)").rsplit(" ")[0]
		if not (f_actual > f_fin):
			docenteAsignado = DocenteResponsableTaller.find_by_ciclo_lectivo_taller_id(ciclo_taller_id)
			if docenteAsignado:
				if(not EstudianteCicloLectivoTaller.find_by_estudiante_id_and_ciclo_lectivo_taller_id(estudiante,ciclo_taller)):
					EstudianteCicloLectivoTaller.db = get_db()
					EstudianteCicloLectivoTaller.create(estudiante, ciclo_taller)
					flash("Se ha asignad")
				else:
					flash("No se pudo realizar la operacion, motivo: El estudiante ya se encuentra asociado a ese taller en ese ciclo lectivo","warning")
					return redirect(url_for("home"))
			else:
				flash("No se pudo realizar la operacion, motivo: El taller no posee docentes asignados para ese ciclo lectivo","warning")
				return redirect(url_for("home"))
		else:
				flash("No se pudo realizar la operacion, motivo: El ciclo lectivo ya termino","warning")
				return redirect(url_for("home"))

'''

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_index', 'docente_show')
def obtener_datos_taller():
	nucleos = Nucleo.query.all()
	cicloLectivoTaller = CicloLectivoTaller.query.all()
	nucleos = [nucleo.serialize() for nucleo in nucleos]
	clts = [clt.serialize() for clt in cicloLectivoTaller if str(CicloLectivo.query.filter_by(id=clt.ciclo_lectivo_id).first().fecha_fin) > str(datetime.datetime.now())]
	dias_all = [horario.serialize() for horario in Horario.query.all()]
	print("all: ", dias_all)
	return jsonify(cicloLectivoTaller=clts, nucleos=nucleos, dias_all=dias_all)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_index', 'docente_show')
def obtener_dias_ciclo_taller():
	try:
		clt_horario_id = request.get_json()['id']
	except AttributeError:
		return jsonify(dias_asign=[], nucleo={"id": "0"})
	dias_asignados_clt = [ Horario.query.filter_by(id=clt_horario.horario_id).first().serialize() for clt_horario in CicloLectivoTallerHorario.query.filter(and_(CicloLectivoTallerHorario.ciclo_lectivo_taller_id==clt_horario_id, CicloLectivoTallerHorario.horario_id!='999')).all()]
	print("dias asignados: ", dias_asignados_clt)

	nucleo_id = CicloLectivoTaller.query.filter_by(id=request.get_json()['id']).first().nucleo_id
	try:
		nucleo = Nucleo.query.filter_by(id=nucleo_id).first().serialize()
	except AttributeError:
		nucleo = {"id": "0"}	
	return jsonify(dias_asign=dias_asignados_clt, nucleo=nucleo)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new', 'administracion_update','administracion_destroy')
def asignar_datos():
	r = request.get_json()["form"]
	# print("clt: ", r["clt"])
	# print("nucleo: ", r["nucleo"])
	# print("dias_ids: ", r["dias_ids"])
	try:
		if int(r["clt"]) in [clta.id for clta in CicloLectivoTaller.query.filter().all()] and int(r["nucleo"]) in [nucleo.id for nucleo in Nucleo.query.filter().all()]:
			CicloLectivoTallerHorario.db = get_db()
			CicloLectivoTaller.db = get_db()

			horarios_tiene = set(str(clth.horario_id) for clth in CicloLectivoTallerHorario.query.filter(and_(CicloLectivoTallerHorario.ciclo_lectivo_taller_id==r["clt"], CicloLectivoTallerHorario.horario_id!='999')).all())
			print(horarios_tiene)
			horarios_nuevos = set(r["dias_ids"])
			horarios_a_borrar = horarios_tiene - horarios_tiene.intersection(horarios_nuevos)
			horarios_a_agregar = horarios_nuevos - horarios_nuevos.intersection(horarios_tiene)

			# print("tiene: ", horarios_tiene)
			# print("nuevos: ", horarios_nuevos)
			# print("borrar: ", horarios_a_borrar)
			# print("agregar: ", horarios_a_agregar)

			for horario in horarios_a_borrar:
				### Hago un borrado logico, pq tira error de constrait key con asistencia al hacer borrado fisico
				CicloLectivoTallerHorario.query.filter_by(ciclo_lectivo_taller_id=r["clt"], horario_id=horario).update(dict(horario_id='999'))

			for horario in horarios_a_agregar:
				### Chequeo si puedo reutilizar algun borrado logico
				clth = CicloLectivoTallerHorario.query.filter(and_(CicloLectivoTallerHorario.ciclo_lectivo_taller_id==r["clt"], CicloLectivoTallerHorario.horario_id=='999')).first()
				if clth:
					clth.horario_id = horario
				else:
					CicloLectivoTallerHorario.db.session.add(CicloLectivoTallerHorario(r["clt"], horario))
			
			clt = CicloLectivoTaller.query.filter_by(id=r["clt"]).update(dict(nucleo_id=r["nucleo"]))

			CicloLectivoTaller.db.session.commit()
			CicloLectivoTallerHorario.db.session.commit()
			flash("Se asignaron los horarios correctamente", "success")
		else:
			flash("Se ingreso un valor inexistente", "warning")
		return jsonify()
	except:
		flash("Ha ocurrido un error", "warning")
		return jsonify()

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_new', 'administracion_update','administracion_destroy')
def asistencia(id_taller):
	### Creo q no se usa 
	print(id_taller)
	flash("entra asistencia", "success")
	Taller.db = get_db()
	talleres = Taller.query.all()
	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
	return render_template('talleres/talleres_index.html', administracion=administracion, talleres=talleres)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_new', 'docente_update','docente_destroy', 'docente_show', 'docente_index')
def registrar_asistencia(ciclo_taller):
	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
	ciclo_taller_obj = CicloLectivoTaller.query.filter_by(id=ciclo_taller).first()
	taller = Taller.query.filter_by(id=ciclo_taller_obj.taller_id).first()
	estudiantes_taller = EstudianteCicloLectivoTaller.query.filter_by(ciclo_lectivo_taller_id=ciclo_taller)
	estudiantes =[]
	for estudiante in estudiantes_taller:
		estudiantes.append(Estudiante.query.filter_by(id=estudiante.estudiante_id).first())
	return render_template('registrar_asistencias.html', administracion=administracion,taller=taller, ciclo_lectivo_taller = ciclo_taller_obj, estudiantes=estudiantes)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_new', 'docente_update','docente_destroy', 'docente_show', 'docente_index')
def registrar_asistencia_estudiante():
	dicdias = {'MONDAY':1,'TUESDAY':2,'WEDNESDAY':3,'THURSDAY':4, \
	'FRIDAY':5,'SATURDAY':6,'SUNDAY':7}
	dia = dicdias[datetime.datetime.now().strftime("%A").upper()]
	taller_horario = CicloLectivoTallerHorario.query.filter_by(ciclo_lectivo_taller_id=request.get_json()['ciclo_lectivo_taller'],horario_id=dia).first()
	db = get_db()
	db.session.add(AsistenciaTallerCicloLectivo(estudiante_id=request.get_json()['estudiante'][11:], dia=datetime.datetime.now(), ciclo_lectivo_taller_horario=taller_horario.id))
	db.session.commit()
	flash('Asistencia tomada correctamente','success')
	return jsonify()


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_new', 'docente_update','docente_destroy', 'docente_show', 'docente_index')
def ver_asistencias(ciclo_taller):
	taller = Taller.query.filter_by(id=CicloLectivoTaller.query.filter_by(id=ciclo_taller).first().taller_id).first()
	clt = CicloLectivoTaller.query.filter_by(id=ciclo_taller).first()
	print(taller)

	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
	clths = CicloLectivoTallerHorario.query.filter_by(ciclo_lectivo_taller_id=ciclo_taller).all()
	dic_asistencias = {}
	for clth in clths:
		print(clth.id)
		l = []
		fechas = []
		for asistencia in AsistenciaTallerCicloLectivo.query.filter_by(ciclo_lectivo_taller_horario=clth.id).all():
			if not (asistencia.dia.strftime("%d/%m/%Y")[:5]) in fechas: # si es una fecha nueva
				l = [] 
			l.append(asistencia.estudiante_id) 
			print(asistencia.estudiante_id)
			
			if not (asistencia.dia.strftime("%d/%m/%Y")[:5]) in fechas: # si es una fecha nueva
				fechas.append((asistencia.dia.strftime("%d/%m/%Y")[:5]))
				dic_asistencias[fechas[-1].replace('/', '')] = l
			else:
				dic_asistencias[fechas[-1].replace('/', '')] = l

	print(dic_asistencias)
	return render_template('talleres/historial_asistencias.html', administracion=administracion, asistencias=dic_asistencias, taller=taller, ciclo_lectivo_taller=clt)
	### Creo q funciona para todos los casos


### Version anterior con Bugs
# def ver_asistencias(ciclo_taller):
# 	from collections import defaultdict
# 	administracion = AdministracionOrquesta.query.filter_by(id='1').first()
# 	from flaskps.models.asistencias import AsistenciaTallerCicloLectivo
# 	from datetime import datetime
# 	clths = CicloLectivoTallerHorario.query.filter_by(ciclo_lectivo_taller_id=ciclo_taller).all()
# 	fechas = []
# 	dic_asistencias = {}
# 	for clth in clths:
# 		print(clth.id)
# 		l = []
# 		fechas = []
# 		for asistencia in AsistenciaTallerCicloLectivo.query.filter_by(ciclo_lectivo_taller_horario=clth.id).all():
# 			print(asistencia.estudiante_id)
# 			l.append(asistencia.estudiante_id)
# 			if not (asistencia.dia.strftime("%d/%m/%Y")[:5]) in fechas:
# 				fechas.append((asistencia.dia.strftime("%d/%m/%Y")[:5]))
# 			dic_asistencias[fechas[-1].replace('/', '')] = l
			
# 	print(dic_asistencias)
# 	return render_template('talleres/historial_asistencias.html', administracion=administracion, ciclo_lectivo_taller = ciclo_taller, asistencias=dic_asistencias)


@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('docente_new', 'docente_update','docente_destroy', 'docente_show', 'docente_index')
def detalle_asistencias():
	import json
	r = json.loads(request.get_json()["ids_estudiantes_asistencias"])
	dic = {}
	for id_est in r:
		estudiante = Estudiante.query.filter_by(id=id_est).first()
		dic[id_est] = estudiante.nombre + ' ' + estudiante.apellido
	print(dic)
	return jsonify(dic=dic) 

