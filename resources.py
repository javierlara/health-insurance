from flask_restful import Resource
from flask import abort, make_response, request
from flask.ext.sqlalchemy import SQLAlchemy
import models
from datetime import datetime

db = SQLAlchemy()

class HealthCenter(Resource):
    @staticmethod
    def get_health_center(health_center_id):
        return db.session.query(models.HealthCenter).get(health_center_id)

    def delete_health_center(self, health_center):
        health_center.deleted_at = datetime.utcnow()
        db.session.commit()

    def update_health_center(self, health_center, data):
        health_center.update(data)
        db.session.commit()

    def get(self, health_center_id):
        health_center = self.get_health_center(health_center_id)
        if health_center is None:
            abort(404)
        return health_center.serialize()

    # @validate_schema(schemas.pickup_rule_creation_request)
    def put(self, health_center_id):
        health_center = self.get_health_center(health_center_id)
        if health_center is None:
            abort(404)
        data = request.get_json()
        self.update_health_center(health_center, data)
        return health_center.serialize()

    def delete(self, health_center_id):
        health_center = self.get_health_center(health_center_id)
        if health_center is None:
            abort(404)
        self.delete_health_center(health_center)
        return make_response()

class HealthCenterCollection(Resource):
    def get(self):
        health_centers = self.get_all_health_centers()
        return [r.serialize() for r in health_centers]

    # @validate_schema(schemas.pickup_rule_creation_request)
    def post(self):
        data = request.get_json()
        new_health_center = self.add_new_health_center(data)
        return new_health_center.serialize()

    def get_all_health_centers(self):
        return db.session.query(models.HealthCenter).all()

    def add_new_health_center(self, data):
        health_center = models.HealthCenter(
            address=data.get('address'),
            telephone=data.get('telephone'),
            extradata=data.get('extradata')
        )

        db.session.add(health_center)
        db.session.commit()

        return health_center