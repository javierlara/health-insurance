from flask.ext.restful import Api
from api import app
from .resources.health_center import HealthCenter, HealthCenterCollection
from .resources.news import NewsCollection, News
from flask import render_template, request, session, redirect, url_for, flash, g
from functools import wraps

api = Api(app)

api.add_resource(HealthCenter, '/api/health_centers/<string:health_center_id>')
api.add_resource(HealthCenterCollection, '/api/health_centers')
api.add_resource(News, '/api/news/<string:news_id>')
api.add_resource(NewsCollection, '/api/news')


def logged():
    return 'logged_in' in session and session['logged_in']


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not logged():
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/health_centers/new', methods=['GET'])
@login_required
def new_center():
    return render_template('newCenter.html')


@app.route('/health_centers', methods=['GET'])
@login_required
def health_centers():
    centers = HealthCenterCollection.get_all_health_centers()
    return render_template('listCenters.html', centers=centers)


@app.route('/health_centers/edit/<int:center_id>', methods=['GET'])
@login_required
def edit_center(center_id):
    center = HealthCenter.get_health_center(center_id)
    return render_template('newCenter.html', center=center)


@app.route('/news/new', methods=['GET'])
@login_required
def new_news():
    return render_template('newNews.html')


@app.route('/news', methods=['GET'])
@login_required
def newses():
    newses = NewsCollection.get_all_news()
    return render_template('listNews.html', newses=newses)


@app.route('/news/edit/<int:news_id>', methods=['GET'])
@login_required
def edit_news(news_id):
    news = News.get_news(news_id)
    return render_template('newNews.html', news=news)


@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    next = request.args.get('next')
    if not next:
        next = url_for('home')
    if 'logged_in' in session and session['logged_in']:
        return redirect(next)
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Usuario inválido'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Contraseña inválida'
        else:
            session['logged_in'] = True
            flash('Iniciaste sesión')
            return redirect(request.form['next'])
    return render_template('login.html', error=error, next=next)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Saliste de la sesión')
    return redirect(url_for('login'))


