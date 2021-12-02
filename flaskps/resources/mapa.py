from flask import redirect, render_template, request, url_for, session, abort, flash, jsonify
from flaskps.db import get_db
from flaskps.helpers.decorators import esta_en_mantenimiento, tiene_permiso, is_authenticated
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.models.taller import Nucleo
import json
from flaskps.resources import auth



@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_show', 'administracion_index')
def index():
	adm = AdministracionOrquesta.query.filter_by(id='1').first()
	nucleos = []
	for nucleo in Nucleo.all() :
		nucleos.append(nucleo.serialize())	
	nucleos = json.dumps(nucleos)	
	
	return render_template("mapa.html",administracion = adm,nucleosPoss = nucleos)

def indexPublico():
	adm = AdministracionOrquesta.query.filter_by(id='1').first()
	nucleos = []
	for nucleo in Nucleo.all() :
		nucleos.append(nucleo.serialize())	
	nucleos = json.dumps(nucleos)	
	
	return render_template("mapaPublico.html",administracion = adm,nucleosPoss = nucleos)

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_show', 'administracion_index')
def setCords():
	r = request.form
	id = r["id"]
	lat = r["lat"]
	lng = r["lng"]	
	Nucleo.db = get_db()
	Nucleo.setCoords(id,lat,lng)
	adm = AdministracionOrquesta.query.filter_by(id='1').first()
	nucleos = []
	for nucleo in Nucleo.all() :
		nucleos.append(nucleo.serialize())	
	nucleos = json.dumps(nucleos)	
	flash("Se agrego la ubicacion correctamente")
	return redirect(url_for("mapa_index"))

@esta_en_mantenimiento
@is_authenticated
@tiene_permiso('administracion_show', 'administracion_index')
def eliminarCords():	
	r = request.form
	id = r["id"]
	Nucleo.db = get_db()
	Nucleo.cleanCords(id)
	return redirect(url_for("mapa_index"))