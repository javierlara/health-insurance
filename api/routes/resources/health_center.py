from flask_restful import Resource
from flask import abort, make_response, request
import api.models as models
from datetime import datetime
from api.db import db_session as session


class HealthCenter(Resource):
    @staticmethod
    def get_health_center(health_center_id):
        return session.query(models.HealthCenter).get(health_center_id)

    @staticmethod
    def delete_health_center(health_center):
        health_center.deleted_at = datetime.utcnow()
        session.commit()

    @staticmethod
    def update_health_center(health_center, data):
        health_center.update(data)
        session.commit()

    def get(self, health_center_id):
        health_center = self.get_health_center(health_center_id)
        if health_center is None:
            abort(404)
        return health_center.serialize()

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

    def post(self):
        data = request.get_json()
        new_health_center = self.add_new_health_center(data)
        return new_health_center.serialize()

    @staticmethod
    def get_all_health_centers():
        query = session.query(models.HealthCenter).filter(models.HealthCenter.deleted_at == None)
        return query.all()

    @staticmethod
    def add_new_health_center(data):
        health_center = models.HealthCenter(
            name=data.get('name'),
            address=data.get('address'),
            telephone=data.get('telephone'),
            location=data.get('location'),
            extradata=data.get('extradata')
        )

        session.add(health_center)
        session.commit()

        return health_center
