import base64

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from api.db import Base
from api.db import db_session as session


class User(Base):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'users'

    # id = Column(Integer, primary_key=True)
    username = Column(String, primary_key=True)
    password = Column(String)
    is_doctor = Column(Boolean, default=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=True)

    def __init__(self, username, password, doctor_id=None):
        self.username = username
        self.password = set_password(password)
        self.doctor_id = doctor_id
        if doctor_id:
            self.is_doctor = True;

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

    def update(self, data):
        self.username = data.get('username')
        password = data.get('password')
        if password:
            encoded_pass = set_password(password)
            print(encoded_pass)
            self.password = encoded_pass
        print(self.password)


    @staticmethod
    def get(username=None):
        print(username)
        if username is None:
            return None
        return session.query(User).filter(User.username == username).first()


def set_password(raw_password):
    return base64.b64encode(raw_password.encode('ascii')).decode("utf-8")


def check_password(raw_password, enc_password):
    if len(enc_password) % 4:
        # not a multiple of 4, add padding:
        enc_password += '=' * (4 - len(enc_password) % 4)
    return raw_password.encode('ascii') == base64.b64decode(enc_password)
