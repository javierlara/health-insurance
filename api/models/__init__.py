from sqlalchemy import Column, Integer, String, DateTime
from api.db import Base
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

class HealthCenter(Base):
    __tablename__ = 'health_centers'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    address = Column(String())
    telephone = Column(String())
    extradata = Column(JSON)
    deleted_at = Column(DateTime())

    def __init__(self, name, address, telephone, extradata, deleted_at):
        self.name = name
        self.address = address
        self.telephone = telephone
        self.extradata = extradata

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'telephone': self.telephone,
            'extradata': self.extradata,
            'deleted_at': str(self.deleted_at)
        }

    def update(self, data):
        self.name = data.get('name')
        self.address = data.get('address')
        self.telephone = data.get('telephone')
        self.extradata = data.get('extradata')