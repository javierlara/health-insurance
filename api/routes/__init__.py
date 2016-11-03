from flask.ext.restful import Api
from api import app
from .resources.health_center import HealthCenter, HealthCenterCollection
from flask import render_template, request, session, redirect, url_for, flash

api = Api(app)

api.add_resource(HealthCenter, '/api/health_centers/<string:health_center_id>')
api.add_resource(HealthCenterCollection, '/api/health_centers')


@app.route('/health_centers/new', methods=['GET'])
def new_center():
    return render_template('newCenter.html')


@app.route('/health_centers', methods=['GET'])
def health_centers():
    centers = HealthCenterCollection.get_all_health_centers()
    return render_template('listCenters.html', centers=centers)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('health_centers'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('health_centers'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
