import sqlalchemy as db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HealthCenter(Base):
    __tablename__ = 'health_centers'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String())
    telephone = db.Column(db.String())
    extradata = db.Column(JSON)

    def __init__(self, address, telephone, extradata):
        self.address = address
        self.telephone = telephone
        self.extradata = extradata

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'telephone': self.telephone,
            'extradata': self.extradata,
        }

    def update(self, data):
        self.address = data.get('address')
        self.telephone = data.get('telephone')
        self.extradata = data.get('extradata')