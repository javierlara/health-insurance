import os
from flask import Flask
from flask_login import LoginManager

from api.db import init_db, db_session
from api.models.user import User

app = Flask(__name__)
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init_db()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


import api.routes


if __name__ == '__main__':
    app.run(debug=True)
