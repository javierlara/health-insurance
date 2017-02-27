import flask as f
from functools import wraps

from flask.ext.login import login_user
from flask.ext.login import logout_user

from api import User, login_manager
from api import app
from api.models.user import check_password


def logged():
    return 'logged_in' in f.session and f.session['logged_in']


def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not logged():
            return f.redirect(f.url_for('login', next=f.request.url))
        return function(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route("/login", methods=["GET", "POST"])
def login():
    next = f.request.args.get('next')
    if not next:
        next = f.url_for('home')
    if 'logged_in' in f.session and f.session['logged_in']:
        return f.redirect(next)
    error = None
    if f.request.method == 'POST':
        username = f.request.form['username']
        password = f.request.form['password']
        user = User.get(username)
        if (user is not None) and check_password(password, user.password):
            login_user(user)
            f.session['logged_in'] = True
            if user.is_doctor:
                return f.redirect(f.url_for('edit_schedule', doctor_id=user.doctor_id))
            return f.redirect(next)
        else:
            if user is None:
                error = 'Usuario inválido'
            else:
                error = 'Contraseña inválida'
    return f.render_template('login.html', error=error, next=next)



@app.route('/logout')
def logout():
    logout_user()
    f.session['logged_in'] = False
    f.flash('Saliste de la sesión')
    return f.redirect(f.url_for('login'))

