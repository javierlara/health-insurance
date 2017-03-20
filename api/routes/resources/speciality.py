from flask_restful import Resource
from flask import abort, make_response, request
import flask as f
import api.models as models
from datetime import datetime
from api.db import db_session as session


class Speciality(Resource):
    @staticmethod
    def get_speciality(speciality_id):
        return session.query(models.Speciality).get(speciality_id)

    @staticmethod
    def delete_speciality(speciality):
        speciality.deleted_at = datetime.utcnow()
        session.commit()

    @staticmethod
    def update_speciality(speciality, data):
        speciality.update(data)
        session.commit()

    def get(self, speciality_id):
        speciality = self.get_speciality(speciality_id)
        if speciality is None:
            abort(404)
        return speciality.serialize()

    def put(self, speciality_id):
        speciality = self.get_speciality(speciality_id)
        if speciality is None:
            abort(404)
        data = request.get_json()
        self.update_speciality(speciality, data)
        f.flash('La especialidad "' + speciality.name + '" fue editada con éxito')
        return speciality.serialize()

    def delete(self, speciality_id):
        speciality = self.get_speciality(speciality_id)
        if speciality is None:
            abort(404)
        self.delete_speciality(speciality)
        f.flash('La especialidad "' + speciality.name + '" fue borrada con éxito')
        return make_response()


class SpecialityCollection(Resource):
    def get(self):
        specialities = self.get_all_specialities()
        return [r.serialize() for r in specialities]

    def post(self):
        data = request.get_json()
        new_speciality = self.add_new_speciality(data)
        f.flash('La especialidad "' + new_speciality.name + '" fue creada con éxito')
        return new_speciality.serialize()

    @staticmethod
    def get_all_specialities():
        query = session.query(models.Speciality).filter(models.Speciality.deleted_at == None)
        return query.all()

    @staticmethod
    def add_new_speciality(data):
        speciality = models.Speciality(
            name=data.get('name'),
            description=data.get('description')
        )

        session.add(speciality)
        session.commit()

        return speciality
