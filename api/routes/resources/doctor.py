from flask_restful import Resource
from flask import abort, make_response, request
import api.models as models
from datetime import datetime
from api.db import db_session as session


class Doctor(Resource):
    @staticmethod
    def get_doctor(doctor_id):
        return session.query(models.Doctor).get(doctor_id)

    @staticmethod
    def delete_doctor(doctor):
        doctor.deleted_at = datetime.utcnow()
        session.commit()

    @staticmethod
    def update_doctor(doctor, data):
        doctor.update(data)
        session.commit()

    def get(self, doctor_id):
        doctor = self.get_doctor(doctor_id)
        if doctor is None:
            abort(404)
        return doctor.serialize()

    def put(self, doctor_id):
        doctor = self.get_doctor(doctor_id)
        if doctor is None:
            abort(404)
        data = request.get_json()
        self.update_doctor(doctor, data)
        return doctor.serialize()

    def delete(self, doctor_id):
        doctor = self.get_doctor(doctor_id)
        if doctor is None:
            abort(404)
        self.delete_doctor(doctor)
        return make_response()


class DoctorCollection(Resource):
    def get(self):
        doctors = self.get_all_doctors()
        return [r.serialize() for r in doctors]

    def post(self):
        data = request.get_json()
        new_doctor = self.add_new_doctor(data)
        return new_doctor.serialize()

    @staticmethod
    def get_all_doctors():
        query = session.query(models.Doctor).filter(models.Doctor.deleted_at == None)
        return query.all()

    @staticmethod
    def add_new_doctor(data):
        doctor = models.Doctor(
            name=data.get('name'),
            address=data.get('address'),
            telephone=data.get('telephone'),
            location=data.get('location'),
            plan_ids=data.get('plan_ids'),
            speciality_ids=data.get('speciality_ids'),
        )

        session.add(doctor)
        session.commit()

        return doctor
