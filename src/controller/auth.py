import functools
from flask import (
    render_template,
    Blueprint,
    g,
    flash,
    redirect,
    request,
    session,
    url_for
)
# security hashes for passwords **
from werkzeug.security import generate_password_hash, check_password_hash

# Maped rows to objects
from src.model.user import User
# import querys
from src.model.repo import *

# Endpoint para la función de autenticación y registro de usuarios
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        birthday = request.form.get('birthday')

        user = get_user(username)
        if not user:
            user = User(username,
                        password,
                        first_name,
                        second_name,
                        birthday)

            add(user)
            return redirect(url_for('home.main'))
        err = 'Username already exists!'
        flash(err)
    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        ok = validate_user_and_password(username, password)
        if ok:
            session.clear()
            session['user'] = username
            return redirect(url_for('home.main'))
        else:
            err = 'Wrong user or password'
            flash(err)
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.clear();
    return redirect(url_for('main'))

@auth.before_app_request
def verify_user():
    '''En cada peticion, verificamos que el usuario este activo'''
    user = session.get('user')
    if user:
        g.user = user
    else:
        g.user = None

def requires_login(foo):
    '''Verifica que hay un login antes de ejecutar el endpoint'''
    @functools.wraps(foo)
    def wrapper(**kwargs):
        if g.user:
            return foo(**kwargs)
        return redirect(url_for('main'))
    return wrapper
