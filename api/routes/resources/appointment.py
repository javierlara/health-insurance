from flask import request, abort
from datetime import datetime
from api import models
from api.db import db_session as session


class Appointment:
    def post(self):
        data = request.get_json()
        new_appointment = self.add_new_appointment(data)
        return new_appointment.serialize()

    def delete(self, appointment_id):
        appointment= self.get_appointment(appointment_id)
        if appointment is None:
            abort(404)
        self.delete_appointment(appointment)
        return appointment.serialize()

    def get_by(self):
        data = request.args
        appointment = self.get_appointment_by(member_id=data.get('member_id'), doctor_id=data.get('doctor_id'))
        if appointment is None:
            abort(404)
        return appointment.serialize()

    @staticmethod
    def get_appointment_by(member_id=None, doctor_id=None):
        query = session.query(models.Appointment)
        if member_id is not None:
            query = query.filter(models.Appointment.member_id == member_id)
        if doctor_id is not None:
            query = query.filter(models.Appointment.doctor_id == doctor_id)
        query = query.filter(models.Appointment.deleted_at == None)
        return query.first()

    @staticmethod
    def get_appointment(appointment_id):
        return session.query(models.Appointment).get(appointment_id)

    @staticmethod
    def delete_appointment(appointment):
        appointment.deleted_at = datetime.utcnow()
        session.commit()

    @staticmethod
    def add_new_appointment(data):
        appointment = models.Appointment(
            doctor_id=data.get('doctor_id'),
            member_id=data.get('member_id'),
            start=data.get('start')
        )
        session.add(appointment)
        session.commit()
        return appointment
