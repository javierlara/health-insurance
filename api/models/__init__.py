import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Table
from sqlalchemy import extract
from sqlalchemy.orm import relationship

from api.db import Base
from sqlalchemy.dialects.postgresql import JSON
from api.db import db_session as session


class HealthCenter(Base):
    __tablename__ = 'health_centers'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    address = Column(String())
    telephone = Column(String())
    location = Column(String())
    extradata = Column(JSON)
    deleted_at = Column(DateTime())

    def __init__(self, name, address, telephone, location, extradata, plan_ids):
        self.name = name
        self.address = address
        self.telephone = telephone
        self.location = location
        self.extradata = extradata
        self.plans = []

        for id in plan_ids:
            plan = session.query(Plan).get(id)
            if plan is not None:
                self.plans.append(plan)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self, relations=True):
        serialized = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'telephone': self.telephone,
            'location': self.location,
            'extradata': self.extradata,
            'deleted_at': str(self.deleted_at)
        }
        if relations:
            serialized['plans'] = [r.serialize(False) for r in self.plans]
        return serialized

    def update(self, data):
        self.name = data.get('name')
        self.address = data.get('address')
        self.telephone = data.get('telephone')
        self.location = data.get('location')
        self.extradata = data.get('extradata')
        self.plans = []
        if data.get('plan_ids') is not None:
            for id in data.get('plan_ids'):
                plan = session.query(Plan).get(id)
                if plan is not None:
                    self.plans.append(plan)


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    image = Column(String())
    content = Column(String())
    author_id = Column(Integer)
    deleted_at = Column(DateTime())

    def __init__(self, title, image, content, author_id):
        self.title = title
        self.image = image
        self.content = content
        self.author_id = author_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image,
            'content': self.content,
            'author_id': self.author_id,
            'deleted_at': str(self.deleted_at)
        }

    def update(self, data):
        self.title = data.get('title')
        self.image = data.get('image')
        self.content = data.get('content')
        self.author_id = data.get('author_id')

health_centers_plans = Table('health_centers_plans',
                             Base.metadata,
                             Column('health_center_id', Integer, ForeignKey('health_centers.id'), nullable=False),
                             Column('plan_id', Integer, ForeignKey('plans.id'), nullable=False),
                             PrimaryKeyConstraint('health_center_id', 'plan_id')
                             )


class Plan(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    deleted_at = Column(DateTime())
    health_centers = relationship('HealthCenter', secondary=health_centers_plans, backref='plans')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        # return '<id {}>'.format(self.id)
        return self.name

    def serialize(self, relations=True):
        serialized = {
            'id': self.id,
            'name': self.name,
            'deleted_at': str(self.deleted_at)
        }
        if relations:
            serialized['health_centers'] = [r.serialize(False) for r in self.health_centers]
            serialized['doctors'] = [r.serialize(False) for r in self.doctors]
        return serialized

    def update(self, data):
        self.name = data.get('name')

class Speciality(Base):
    __tablename__ = 'specialities'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    description = Column(String())
    deleted_at = Column(DateTime())

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self, relations=True):
        serialized = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'deleted_at': str(self.deleted_at)
        }
        if relations:
            serialized['doctors'] = [r.serialize(False) for r in self.doctors]
        return serialized

    def update(self, data):
        self.name = data.get('name')
        self.description = data.get('description')

doctors_plans = Table('doctors_plans',
                             Base.metadata,
                             Column('doctor_id', Integer, ForeignKey('doctors.id'), nullable=False),
                             Column('plan_id', Integer, ForeignKey('plans.id'), nullable=False),
                             PrimaryKeyConstraint('doctor_id', 'plan_id')
                             )

doctors_specialities = Table('doctors_specialities',
                             Base.metadata,
                             Column('doctor_id', Integer, ForeignKey('doctors.id'), nullable=False),
                             Column('speciality_id', Integer, ForeignKey('specialities.id'), nullable=False),
                             PrimaryKeyConstraint('doctor_id', 'speciality_id')
                             )


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    address = Column(String())
    telephone = Column(String())
    location = Column(String())
    plans = relationship('Plan', secondary=doctors_plans, backref='doctors')
    specialities = relationship('Speciality', secondary=doctors_specialities, backref='doctors')
    deleted_at = Column(DateTime())
    user_id = Column(Integer)

    def __init__(self, name, address, telephone, location, plan_ids, speciality_ids):
        self.name = name
        self.address = address
        self.telephone = telephone
        self.location = location

        if plan_ids is not None:
            for p_id in plan_ids:
                plan = session.query(Plan).get(p_id)
                if plan is not None:
                    self.plans.append(plan)
        if speciality_ids is not None:
            for s_id in speciality_ids:
                speciality = session.query(Speciality).get(s_id)
                if speciality is not None:
                    self.specialities.append(speciality)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self, relations=True):
        serialized = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'telephone': self.telephone,
            'location': self.location,
            'deleted_at': str(self.deleted_at)
        }
        if relations:
            serialized['plans'] = [r.serialize(False) for r in self.plans]
            serialized['specialities'] = [r.serialize(False) for r in self.specialities]
        if hasattr(self, 'distance'):
            serialized['distance'] = self.distance
        return serialized

    def update(self, data):
        self.name = data.get('name')
        self.address = data.get('address')
        self.telephone = data.get('telephone')
        self.location = data.get('location')
        self.plans = []
        self.specialities = []
        if data.get('plan_ids') is not None:
            for p_id in data.get('plan_ids'):
                plan = session.query(Plan).get(p_id)
                if plan is not None:
                    self.plans.append(plan)
        if data.get('speciality_ids') is not None:
            for s_id in data.get('speciality_ids'):
                speciality = session.query(Speciality).get(s_id)
                if speciality is not None:
                    self.specialities.append(speciality)


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    address = Column(String())
    telephone = Column(String())
    plan_id = Column(Integer, ForeignKey('plans.id'))
    deleted_at = Column(DateTime())
    member_number = Column(Integer)
    plan = relationship('Plan', foreign_keys=plan_id)

    def __init__(self, name, address, telephone, plan_id, member_number):
        self.name = name
        self.address = address
        self.telephone = telephone
        self.plan_id = plan_id
        self.member_number = member_number

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'telephone': self.telephone,
            'plan_id': self.plan_id,
            'member_number' : self.member_number,
            'deleted_at': str(self.deleted_at)
        }

    def update(self, data):
        self.name = data.get('name')
        self.address = data.get('address')
        self.telephone = data.get('telephone')
        self.plan_id = data.get('plan_id')
        self.member_number = data.get('member_number')


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    member_id = Column(Integer, ForeignKey('members.id'))
    start = Column(DateTime())
    end = Column(DateTime())
    deleted_at = Column(DateTime())

    def __init__(self, doctor_id, member_id, start, end=None):
        self.doctor_id = doctor_id
        self.member_id = member_id
        self.start = datetime.datetime.fromtimestamp(float(start)/1000.0)
        if end is None:
            end = start + (30*60*1000) # agrego media hora
        self.end = datetime.datetime.fromtimestamp(float(end)/1000.0)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'member_id': self.member_id,
            'start': self.start,
            'end': self.end,
            'deleted_at': str(self.deleted_at)
        }

    def update(self, data):
        self.doctor_id = data.get('doctor_id')
        self.member_id = data.get('member_id')
        self.start = data.get('start')
        self.end = data.get('end')


class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    start = Column(DateTime())
    end = Column(DateTime())
    deleted_at = Column(DateTime())

    def __init__(self, doctor_id, start, end):
        self.doctor_id = doctor_id
        self.start = datetime.datetime.fromtimestamp(float(start)/1000.0)
        self.end = datetime.datetime.fromtimestamp(float(end)/1000.0)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'start': str(self.start),
            'end': str(self.end),
            'deleted_at': str(self.deleted_at)
        }

    def getDay(self):
        return {
            'day': self.start.day
        }

    def update(self, data):
        self.start = datetime.datetime.fromtimestamp(float(data.get('start'))/1000.0)
        self.end = datetime.datetime.fromtimestamp(float(data.get('end'))/1000.0)

    def get_slots(self):
        query = session.query(Appointment) \
            .filter(Appointment.doctor_id == self.doctor_id) \
            .filter(extract('day', Appointment.start) == self.start.day) \
            .filter(extract('month', Appointment.start) == self.start.month) \
            .filter(extract('year', Appointment.start) == self.start.year) \
            .filter(Appointment.deleted_at == None)
        appointments = query.all()
        slots = self.get_available_slots(appointments)
        return {
            'day': self.start.day,
            'slots': [{'start': s.start, 'end': s.end} for s in slots]
        }

    def get_available_slots(self, appointments):
        schedules = []
        appointments_slots = []
        delta = datetime.timedelta(minutes=30)

        for schedule in Slot.perdelta(self.start, self.end, delta):
            schedules.append(Slot(schedule, schedule + delta))

        for appointment in appointments:
            appointments_slots.append(Slot(appointment.start, appointment.end))

        available_slots = list(set(schedules) - set(appointments_slots))
        available_slots.sort(key=lambda r: r.start)

        return available_slots


class Slot:
    start = ''
    end = ''

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return str(self.start) + ' - ' + str(self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return int(self.start.timestamp()*1000)

    @staticmethod
    def perdelta(start, end, delta):
        curr = start
        while curr < end:
            yield curr
            curr += delta
