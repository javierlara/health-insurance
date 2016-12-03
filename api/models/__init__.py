from sqlalchemy import Column, Integer, String, DateTime
from api.db import Base
from sqlalchemy.dialects.postgresql import JSON


class HealthCenter(Base):
    __tablename__ = 'health_centers'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    address = Column(String())
    telephone = Column(String())
    location = Column(String())
    extradata = Column(JSON)
    deleted_at = Column(DateTime())

    def __init__(self, name, address, telephone, location, extradata):
        self.name = name
        self.address = address
        self.telephone = telephone
        self.location = location
        self.extradata = extradata

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'telephone': self.telephone,
            'location': self.location,
            'extradata': self.extradata,
            'deleted_at': str(self.deleted_at)
        }

    def update(self, data):
        self.name = data.get('name')
        self.address = data.get('address')
        self.telephone = data.get('telephone')
        self.location = data.get('location')
        self.extradata = data.get('extradata')


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
