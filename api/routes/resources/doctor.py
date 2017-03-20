from flask_restful import Resource
from flask import abort, make_response, request
import flask as f
import api.models as models
from datetime import datetime

from api import User
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
        if doctor.user:
            doctor.user.update(data)
        else:
            user = User(
                username=data.get('username'),
                password=data.get('password'),
                doctor_id=doctor.id
            )
            session.add(user)
        print(doctor.user.password)
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
        f.flash('El prestador "' + doctor.name + '" fue editado con éxito')
        return doctor.serialize()

    def delete(self, doctor_id):
        doctor = self.get_doctor(doctor_id)
        if doctor is None:
            abort(404)
        self.delete_doctor(doctor)
        f.flash('El prestador "' + doctor.name + '" fue borrado con éxito')
        return make_response()


class DoctorCollection(Resource):
    def get(self):
        doctors = self.get_all_doctors()
        return [r.serialize() for r in doctors]

    def post(self):
        data = request.get_json()
        new_doctor = self.add_new_doctor(data)
        f.flash('El prestador "' + new_doctor.name + '" fue creado con éxito')
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

        user = User(
            username=data.get('username'),
            password=data.get('password'),
            doctor_id=doctor.id
        )

        session.add(user)
        session.commit()

        return doctor
