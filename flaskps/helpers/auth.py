from flaskps.resources import auth

def authenticated(session):
    return session.get('user')

def admin(session):
    return auth.is_admin(session.get("user"))
def es_docente(session):
    return auth.is_admin(session.get("user"),'docente')
def es_preceptor(session):
    return auth.is_admin(session.get('user'),'preceptor')



