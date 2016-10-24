import os
from flask import Flask
from flask.ext.restful import Api
from resources import db, HealthCenter, HealthCenterCollection

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

api.add_resource(HealthCenter, '/health_centers/<string:health_center_id>')
api.add_resource(HealthCenterCollection, '/health_centers')

if __name__ == '__main__':
    app.run(debug=True)
