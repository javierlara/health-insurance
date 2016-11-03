import os
from flask import Flask
from api.db import init_db, db_session

app = Flask(__name__)
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import api.routes

if __name__ == '__main__':
    app.run(debug=True)
