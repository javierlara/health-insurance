from flask import request

from api import models
from api.db import db_session as session


class Appointment:
    def post(self):
        data = request.get_json()
        new_appointment = self.add_new_appointment(data)
        return new_appointment.serialize()

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
