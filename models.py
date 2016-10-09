from app import db
from sqlalchemy.dialects.postgresql import JSON


class HealthCenter(db.Model):
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