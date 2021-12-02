import os
from os import path
from flask import redirect, render_template, request, url_for, session, abort, flash,jsonify
from flask import Flask, render_template, g, abort
from flask_session import Session
from flaskps.resources import user, auth, estudiante, docente, cicloLectivo, taller,instrumento, mapa
from flaskps.config import Config
from flaskps.helpers import handler
from flaskps.helpers import auth as helper_auth
from flaskps.models.shared import db
from flaskps.models.estudiante import *
from flaskps.models.docente import *
from flaskps.models.instrumento import *
from flaskps.models.estudianteCicloLectivoTaller import EstudianteCicloLectivoTaller
from flaskps.models.administracion_orquesta import AdministracionOrquesta
from flaskps.models.asistencias import *
from flaskps.models.user import *
from flaskps.db import get_db
from flaskps.const import UPLOAD_FOLDER
#from flaskps.models import cicloLectivo, cicloLectivoTaller, taller, docenteResponsableTaller

from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
from flask_login import logout_user, current_user, LoginManager
from flask_login import login_required, login_user
import os

# Configuración inicial de la app
app = Flask(__name__,static_url_path='', static_folder="static")
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = "{}+{}://{}:{}@{}:{}/{}".format("mysql","pymysql","root","aluminio9","localhost","3306","grupo35")
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


#Server Side session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
Session(app)


# Funciones que se exportan al contexto de Jinja2
app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
app.jinja_env.globals.update(is_admin=helper_auth.admin)
app.jinja_env.globals.update(es_preceptor=helper_auth.es_preceptor)
app.jinja_env.globals.update(es_docente=helper_auth.es_docente)

# Autenticación
app.add_url_rule("/iniciar_sesion", 'auth_login', auth.login, methods=['GET', 'POST'])
app.add_url_rule("/cerrar_sesion", 'auth_logout', auth.logout)
app.add_url_rule(
    "/autenticacion",
    'auth_authenticate',
    auth.authenticate,
    methods=['POST']
)
app.add_url_rule("/home", 'home', user.home)
# Usuarios
app.add_url_rule("/usuarios", 'user_index', user.index)
app.add_url_rule("/usuarios", 'user_create', user.create, methods=['POST'])
app.add_url_rule("/usuarios/nuevo", 'user_new', user.new)
app.add_url_rule("/usuario/editing_form", 'user_edit_form', user.edit_form,methods=['POST'])
app.add_url_rule("/usuario/editar", 'user_edit', user.edit, methods=['POST'])
app.add_url_rule("/usuario/user_state_toggle", 'user_state_toggle', user.state_toggle, methods=['POST'])
app.add_url_rule("/usuario/user_delete", 'user_delete', user.user_delete, methods=['POST'])
app.add_url_rule("/usuarios/", 'user_search', user.search, methods=['GET'])
app.add_url_rule("/usuarios/check_username", 'check_username', user.check_username, methods=['POST'])
app.add_url_rule("/usuarios/check_email", 'check_email', user.check_email, methods=['POST'])

# Modulo de instrumentos
app.add_url_rule("/instrumentos/", "instrumentos", instrumento.crud_instrumento , methods=['GET', 'POST'])
app.add_url_rule("/instrumentos/detalle_instrumento", "detalle_instrumento", instrumento.detalle_instrumento, methods=['POST'])
app.add_url_rule("/instumentos/eliminar_instrumento", "eliminar_instrumento", instrumento.eliminar_instrumento, methods=['POST'])
app.add_url_rule("/instrumentos/modificar_instrumento", "modificar_instrumento", instrumento.modificar_instrumento, methods=['POST'])
app.add_url_rule("/instrumentos/crear_instrumento", "crear_instrumento", instrumento.crear_instrumento, methods=['POST'])
app.add_url_rule("/instrumentos/inventario_instrumento", "numero_inventario_instrumento", instrumento.numero_inventario_instrumento, methods=['POST'])
# Modulo de estudiantes
app.add_url_rule("/estudiantes/", "estudiantes", estudiante.crud_estudiantes, methods=['GET', 'POST'])
app.add_url_rule("/estudiantes/crear_estudiante", "crear_estudiante", estudiante.crear_estudiantes, methods=['POST'])
app.add_url_rule("/estudiantes/eliminar_estudiante", "eliminar_estudiante", estudiante.eliminar_estudiante, methods=['POST'])
app.add_url_rule("/estudiantes/detalle_estudiante", "detalle_estudiante", estudiante.detalle_estudiante, methods=['POST'])
app.add_url_rule("/estudiantes/modificar_estudiante", "modificar_estudiante", estudiante.modificar_estudiante, methods=['POST'])
app.add_url_rule("/estudiantes/documento_estudiante", "documento_estudiante", estudiante.documento_estudiante, methods=['POST'])

# Modulo de Docentes
app.add_url_rule("/docentes/", "docentes", docente.crud_docentes, methods=['GET', 'POST'])
app.add_url_rule("/docentes/eliminar_docente", "eliminar_docente", docente.eliminar_docente, methods=['POST'])
app.add_url_rule("/docentes/detalle_docente", "detalle_docente", docente.detalle_docente, methods=['POST'])
app.add_url_rule("/docentes/modificar_docente", "modificar_docente", docente.modificar_docente, methods=['POST'])
app.add_url_rule("/docentes/documento_docente", "documento_docente", docente.documento_docente, methods=['POST'])

# Modulo De Configuracion
app.add_url_rule("/configuracion/", "configuracion", user.configure, methods=['GET', 'POST'])
app.add_url_rule("/configuracion/activo_desactivo_sitio", "activo_desactivo_sitio", user.activo_desactivo_sitio, methods=['GET', 'POST'])

#Modulo Administrativo
app.add_url_rule("/ciclos/", "ciclos", cicloLectivo.index, methods=['GET', 'POST'])
app.add_url_rule("/ciclos/edit", "ciclo_edit", cicloLectivo.edit, methods=['GET', 'POST'])
app.add_url_rule("/ciclos/new", "ciclo_new", cicloLectivo.new, methods=['GET', 'POST'])
app.add_url_rule("/ciclos/create", "ciclo_create", cicloLectivo.create, methods=['GET', 'POST'])
app.add_url_rule("/ciclos/delete", "ciclo_delete", cicloLectivo.delete, methods=['GET', 'POST'])
app.add_url_rule("/ciclos/asignar_taller/", "asignar_taller_a_ciclo", cicloLectivo.asignar_taller_a_ciclo, methods=['POST'])
app.add_url_rule("/ciclos/ver_talleres","ver_talleres",cicloLectivo.ver_talleres)
app.add_url_rule("/ciclos/desasignar_taller","desasignar_taller",cicloLectivo.desasignar_taller, methods=['POST'])
app.add_url_rule("/asignacion_horarios/configurar/","ciclo_taller_nucleo_dias", taller.asignar_datos, methods=['POST'])
app.add_url_rule("/asignacion_horarios/", "obtener_datos_taller", taller.obtener_datos_taller, methods=['POST'])
app.add_url_rule("/asignacion_horarios/solo_ajax/", "obtener_dias_ciclo_taller", taller.obtener_dias_ciclo_taller, methods=['POST'])

# Modulo de Talleres
app.add_url_rule("/talleres/", "talleres", taller.index, methods=['GET', 'POST'])
app.add_url_rule("/talleres/editar", "taller_edit", taller.edit, methods=['GET', 'POST'])
app.add_url_rule("/talleres/asignar_estudiantes","asignar_estudiantes",taller.asignarEstudiante, methods=['GET','POST'])

app.add_url_rule("/talleres/asistencia/<int:ciclo_taller>/", "registrar_asistencias", taller.registrar_asistencia, methods=["GET", "POST"])
app.add_url_rule("/talleres/registrar_asistencia_estudiante", "registrar_asistencia_estudiante", taller.registrar_asistencia_estudiante, methods=["POST"])
app.add_url_rule("/talleres/ver_asistencias/<ciclo_taller>/", "ver_asistencias_clt", taller.ver_asistencias, methods=["GET", "POST"])
app.add_url_rule("/talleres/ver_asistencias/detalle_asistencias/", "detalle_asistencias", taller.detalle_asistencias, methods=["GET", "POST"])

#Funcionalidad libre Mapa
app.add_url_rule("/mapa","mapa_index",mapa.index,methods=['GET'])
app.add_url_rule("/mapa/create","mapa_setCords",mapa.setCords,methods=['POST'])
app.add_url_rule("/mapa/eliminarCords","mapa_eliminarCords",mapa.eliminarCords,methods=['POST'])
app.add_url_rule("/mapaPublico","mapa_publico",mapa.indexPublico,methods=['GET'])

@app.route("/")
def to_home():
    return redirect(url_for("home"))


github_blueprint = make_github_blueprint(client_id='559d8368c7935ab4e015', client_secret='157a6d7fb05bc9302b9ab091e3d3d514990f2654')
app.register_blueprint(github_blueprint, url_prefix='/github_login')


class OAuth(OAuthConsumerMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    provider_user_id = db.Column(db.String(255), nullable=False)
    provider_user_login = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship("User", cascade="all, delete-orphan", single_parent=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

github_blueprint.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user, user_required=False)

@app.route('/github')
def github_login():
    if not github.authorized:
        # va a la pantalla de autorizacion
        return redirect(url_for('github.login')) #llama al github_logged_in
    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        session['user'] = account_info_json['login']
        flash("La sesión se inició correctamente.", "success")
        return redirect(url_for('home'))

    # ocurre un error
    flash("Ha ocurrido un error", "warning")
    return redirect(url_for('home'))

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    if not token:
        flash("No se Pudo Iniciar Sesion con GitHub", "warning")
        # return
        return redirect(url_for('home'))

    resp = blueprint.session.get("/user")
    if not resp.ok:
        msg = "Error al Recuperar datos del Usuario"
        flash(msg, "warning")
        # return
        return redirect(url_for('home'))

    github_info = resp.json()
    github_user_id = str(github_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name, provider_user_id=github_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        github_user_login = str(github_info["login"])
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=github_user_id,
            provider_user_login=github_user_login,
            token=token,
        )

    # Now, figure out what to do with this token. There are 2x2 options:
    # user login state and token link state.

    if current_user.is_anonymous:
        if oauth.user:
            # If the user is not logged in and the token is linked,
            # log the user into the linked user account
            login_user(oauth.user)
            session['user'] = github_info['login']
            flash("Sesion Iniciada correctamente con GitHub", "success")
        else:
            # If the user is not logged in and the token is unlinked,
            # create a new local user account and log that account in.
            # This means that one person can make multiple accounts, but it's
            # OK because they can merge those accounts later.
           
            # if github_info["email"] != None:
            #     user = User(github_info["email"], None, github_info["name"], None, github_info["login"])
            # else:
            #     print("entrererte")
            #     user = User("", None, "", None, github_info["login"])
            
            user = User(github_info["email"] if github_info["email"] != None else "", None, github_info["name"] if github_info["name"] != None else "", "", github_info["login"])
            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)
            session['user'] = github_info['login']
            flash("Sesión Iniciada correctamente con GitHub", "success")
    else:
        if oauth.user: # Creo q nunca entraria
            # If the user is logged in and the token is linked, check if these
            # accounts are the same!
            if current_user != oauth.user:
                # Account collision! Ask user if they want to merge accounts.
                url = url_for("auth.merge", username=oauth.user.username)
                return redirect(url)
        else:
            # If the user is logged in and the token is unlinked,
            # link the token to the current user
            oauth.user = current_user
            db.session.add(oauth)
            db.session.commit()
            session['user'] = github_info['login']
            flash("GitHub enlazado correctamente", "success")

    # Indicate that the backend shouldn't manage creating the OAuth object
    # in the database, since we've already done so!
    return False


# notify on OAuth provider error
@oauth_error.connect_via(github_blueprint)
def github_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, "warning")



# OAuth configuration
# CLIENT_ID = ('54425504-i1u5ufd37shfu6a1lgct15kef9mu4ebh' '.apps.googleusercontent.com')
# CLIENT_SECRET = 'SeUhtUIzQgJQ2Vob-ROK'
# REDIRECT_URI = 'https://localhost:5000/gCallback'
# AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
# TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
# USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
# SCOPE = ['profile', 'email']

# class GoogleLogin():
#     default_scope = (
#         "https://www.googleapis.com/auth/userinfo.email,"
#         "https://www.googleapis.com/auth/userinfo.profile"
#     )
#     default_redirect_path = "/login/google"

#     auth_url = "https://accounts.google.com/o/oauth2/auth"
#     token_url = "https://accounts.google.com/o/oauth2/token"
#     profile_url = "https://www.googleapis.com/oauth2/v2/userinfo"

# # OAuth 2 client setup
# client = WebApplicationClient(GOOGLE_CLIENT_ID)

# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()


# @app.route("/login")
# def login():
#     # Find out what URL to hit for Google login
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]

#     # Use library to construct the request for Google login and provide
#     # scopes that let you retrieve user's profile from Google
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)


# @app.route("/login/callback")
# def callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get("code")


# def get_google_auth(state=None, token=None):
#     if token:
#         return OAuth2Session(Auth.CLIENT_ID, token=token)
#     if state:
#         return OAuth2Session( CLIENT_ID, state=state, redirect_uri=REDIRECT_URI)
#     oauth = OAuth2Session( CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
#     return oauth

# @app.route('/login')
# def login():
#     User.db=get_db()
#     user= User.query.filter_by(email=session.get("user")).first()
#     if user:
#         return redirect(url_for('index'))
#     google = get_google_auth()
#     auth_url, state = google.authorization_url( AUTH_URI, access_type='offline')
#     session['oauth_state'] = state
#     return render_template('auth/login_template.html', administracion=AdministracionOrquesta.query.filter_by(id=1), auth_url=auth_url)


# @app.route('/gCallback')
# def callback():
#     # Redirect user to home page if already logged in.
#     User.db=get_db()
#     user= User.query.filter_by(email=session.get("user")).first()
#     if user:
#         print("aaaaaa")
#         return redirect(url_for('index'))
#     if 'error' in request.args:
#         if request.args.get('error') == 'access_denied':
#             return 'You denied access.'
#         return 'Error encountered.'
#     if 'code' not in request.args and 'state' not in request.args:
#         return redirect(url_for('login'))
#     else:
#         # Execution reaches here when user has successfully authenticated our app.
#         google = get_google_auth(state=session['oauth_state'])
#         try:
#             token = google.fetch_token( TOKEN_URI, client_secret=CLIENT_SECRET, authorization_response=request.url)
#         except HTTPError:
#             return 'HTTPError occurred.'
#         google = get_google_auth(token=token)
#         resp = google.get(USER_INFO)
#         if resp.status_code == 200:
#             user_data = resp.json()
#             email = user_data['email']
#             user = User.query.filter_by(email=email).first()
#             if user is None:
#                 user = User()
#                 user.email = email
#             user.name = user_data['name']
#             user.tokens = json.dumps(token)
#             user.avatar = user_data['picture']
#             db.session.add(user)
#             db.session.commit()
#             login_user(user)
#             return redirect(url_for('index'))
#         return 'Could not fetch your information.'

# @app.route("/configuracion/", methods=['GET', 'POST'])
# def configuracion():
#     print("entra a app.route")
#     if not helper_auth.authenticated or not helper_auth.admin:
#         abort(401)
#     if request.method == "POST":
#         print(request.form["search_user"])
#         return render_template("home2.html")
#     else:
#         return render_template("/user/config_template.html")
# Handlers
app.register_error_handler(404, handler.not_found_error)
app.register_error_handler(401, handler.unauthorized_error)
app.register_error_handler(500, handler.not_found_error)
app.register_error_handler(409, handler.inactive_user_error)
app.register_error_handler(405, handler.method_not_allowed_error)
# Implementar lo mismo para el error 500 y 401
