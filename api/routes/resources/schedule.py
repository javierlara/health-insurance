import datetime
import sys

import pytz
from flask import request
from flask.ext.restful import abort, Resource

from api import models
from api.db import db_session as session
from sqlalchemy import extract


class Schedule():

    @staticmethod
    def get_schedule(doctor_id, miliseconds):
        date_query = datetime.datetime.fromtimestamp(float(miliseconds) / 1000.0, tz=pytz.utc)
        query = session.query(models.Schedule) \
            .filter(models.Schedule.doctor_id == doctor_id) \
            .filter(extract('day', models.Schedule.start) == date_query.day)\
            .filter(extract('month', models.Schedule.start) == date_query.month)\
            .filter(extract('year', models.Schedule.start) == date_query.year)\
            .filter(models.Schedule.deleted_at == None)
        return query.first()

    @staticmethod
    def add_new_schedule(doctor_id, data):
        schedule = models.Schedule(
            doctor_id=doctor_id,
            start=data.get('start'),
            end=data.get('end')
        )
        session.add(schedule)
        session.commit()
        return schedule

    @staticmethod
    def update_schedule(schedule, data):
        schedule.update(data)
        session.commit()

    def get(self, doctor_id, miliseconds):
        # print(doctor_id, file=sys.stderr)
        schedule = self.get_schedule(doctor_id, miliseconds)
        if schedule is None:
            return {'success': False}
        return {'success': True, 'payload': schedule.serialize()}

    def post(self, doctor_id):
        data = request.get_json()
        new_schedule = self.add_new_schedule(doctor_id, data)
        print(new_schedule.serialize(), file=sys.stderr)
        return new_schedule.serialize()

    def put(self, doctor_id):
        data = request.get_json()
        schedule = self.get_schedule(doctor_id, data.get('start'))
        if schedule is None:
            abort(404)
        self.update_schedule(schedule, data)
        return schedule.serialize()

    @staticmethod
    def getDays(doctor_id, month, year):
        query = session.query(models.Schedule) \
            .filter(models.Schedule.doctor_id == doctor_id) \
            .filter(extract('month', models.Schedule.start) == month) \
            .filter(extract('year', models.Schedule.start) == year) \
            .filter(models.Schedule.deleted_at == None)
        schedules = query.all()
        return {'success': True, 'payload': [r.getDay() for r in schedules]}

    @staticmethod
    def getMonthSchedule(doctor_id, month, year):
        query = session.query(models.Schedule) \
            .filter(models.Schedule.doctor_id == doctor_id) \
            .filter(extract('month', models.Schedule.start) == month) \
            .filter(extract('year', models.Schedule.start) == year) \
            .filter(models.Schedule.deleted_at == None)
        schedules = query.all()
        return {'success': True, 'payload': [r.get_slots() for r in schedules]}

    @staticmethod
    def getAvailableSchedule(doctor_id, month, year):
        query = session.query(models.Schedule) \
            .filter(models.Schedule.doctor_id == doctor_id) \
            .filter(extract('month', models.Schedule.start) == month) \
            .filter(extract('year', models.Schedule.start) == year) \
            .filter(models.Schedule.deleted_at == None)
        schedules = query.all()
        return {'success': True, 'payload': [r.getSchedule() for r in schedules]}
