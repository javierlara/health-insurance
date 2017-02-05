import base64

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from api.db import Base
from api.db import db_session as session


class User(Base):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, primary_key=True)
    password = Column(String)
    is_doctor = Column(Boolean, default=False)
    doctor_id = Column(Integer, nullable=True)

    def __init__(self, username, password):
        self.id = id
        self.username = username
        self.password = set_password(password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.username)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')



    @staticmethod
    def get(username=None):
        print(username)
        if username is None:
            return None
        return session.query(User).filter(User.username == username).first()


def set_password(raw_password):
    return base64.b64encode(raw_password.encode('ascii'))


def check_password(raw_password, enc_password):
    return raw_password.encode('ascii') == base64.b64decode(enc_password)
