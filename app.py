import os
from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import HealthCenter


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    if request.method == "POST":
        # get url that the person has entered
        try:
            address = request.form['address']
        except:
            errors.append(
                "Unable to get Address. Please make sure it's valid and try again."
            )
            return render_template('index.html', errors=errors)
        try:
            center = HealthCenter(
                address=address,
                telephone=None,
                extradata=None
            )
            db.session.add(center)
            db.session.commit()
        except:
            errors.append("Unable to add item to database.")
            raise
    return render_template('index.html', errors=errors)


if __name__ == '__main__':
    app.run()