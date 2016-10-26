from flask.ext.restful import Api
from api import app
from .resources.health_center import HealthCenter, HealthCenterCollection

api = Api(app)

api.add_resource(HealthCenter, '/health_centers/<string:health_center_id>')
api.add_resource(HealthCenterCollection, '/health_centers')