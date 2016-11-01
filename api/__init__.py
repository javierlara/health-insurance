import os
from flask import Flask, render_template
# from flask.ext.sqlalchemy import SQLAlchemy
from api.db import init_db, db_session

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import api.routes


@app.route('/health_centers/new', methods=['GET'])
def newCenter():
    return render_template('newCenter.html')

@app.route('/health_centers', methods=['GET'])
def index():
    return render_template('listCenters.html')

if __name__ == '__main__':
    app.run(debug=True)
