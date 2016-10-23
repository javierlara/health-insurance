import os
from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Resource, Api
import models


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

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

todos = {}

class HealthCenter(Resource):
    def get(self, center_id):
        health_center = db.session.query(models.HealthCenter).get(center_id)
        if health_center is None:
            abort(404)
        return health_center.serialize()

    # def put(self, center_id):
    #     todos[center_id] = request.form['data']
    #     return {center_id: todos[center_id]}

api.add_resource(HealthCenter, '/health_center/<string:center_id>')

if __name__ == '__main__':
    app.run(debug=True)
