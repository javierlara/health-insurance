from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Table
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
        return '<id {}>'.format(self.id)

    def serialize(self, relations=True):
        serialized = {
            'id': self.id,
            'name': self.name,
            'deleted_at': str(self.deleted_at)
        }
        if relations:
            serialized['health_centers'] = [r.serialize(False) for r in self.health_centers]
        return serialized

    def update(self, data):
        self.name = data.get('name')

doctors_plans = Table('doctors_plans',
                             Base.metadata,
                             Column('doctor_id', Integer, ForeignKey('doctors.id'), nullable=False),
                             Column('plan_id', Integer, ForeignKey('plans.id'), nullable=False),
                             PrimaryKeyConstraint('doctor_id', 'plan_id')
                             )


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    address = Column(String())
    telephone = Column(String())
    location = Column(String())
    plans = relationship('Plan', secondary=doctors_plans, backref='doctors')
    deleted_at = Column(DateTime())

    def __init__(self, name, address, telephone, location, plan_ids):
        self.name = name
        self.address = address
        self.telephone = telephone
        self.location = location

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
        self.plans = []
        if data.get('plan_ids') is not None:
            for id in data.get('plan_ids'):
                plan = session.query(Plan).get(id)
                if plan is not None:
                    self.plans.append(plan)

