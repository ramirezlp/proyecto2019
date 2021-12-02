from flask import render_template

def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe"
    }
    return render_template('error.html', **kwargs), 404

def method_not_allowed_error(e):
    kwargs = {
        "error_name": "405 Method not allowed",
        "error_description": "No esta autorizada su petición"
    }
    return render_template('error.html', **kwargs), 405

def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url"
    }
    return render_template('error.html', **kwargs), 401

def inactive_user_error(e):
    kwargs = {
        "error_name": "409 Inactive user Error",
        "error_description": "SU USUARIO SE ENCUENTRA INACTIVO"
    }
    return render_template('error.html', **kwargs), 409
