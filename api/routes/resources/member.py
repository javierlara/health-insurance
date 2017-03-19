from flask_restful import Resource
from flask import abort, make_response, request
import flask as f
import api.models as models
from datetime import datetime
from api.db import db_session as session


class Member(Resource):
    @staticmethod
    def get_member(member_id):
        return session.query(models.Member).get(member_id)

    @staticmethod
    def get_member_by_number(member_number):
        query = session.query(models.Member) \
            .filter(models.Member.member_number == member_number) \
            .filter(models.Member.deleted_at == None)
        return query.first()

    @staticmethod
    def delete_member(member):
        member.deleted_at = datetime.utcnow()
        session.commit()

    @staticmethod
    def update_member(member, data):
        member.update(data)
        session.commit()

    def get_by_number(self, member_number):
        member = self.get_member_by_number(member_number)
        if member is None:
            abort(404)
        return member.serialize()

    def get(self, member_id):
        member = self.get_member(member_id)
        if member is None:
            abort(404)
        return member.serialize()

    def put(self, member_id):
        member = self.get_member(member_id)
        if member is None:
            abort(404)
        data = request.get_json()
        self.update_member(member, data)
        f.flash('El socio "' + member.name + '" fue editado con éxito')
        return member.serialize()

    def delete(self, member_id):
        member = self.get_member(member_id)
        if member is None:
            abort(404)
        self.delete_member(member)
        f.flash('El socio "' + member.name + '" fue borrado con éxito')
        return make_response()


class MemberCollection(Resource):
    def get(self):
        members = self.get_all_members()
        return [r.serialize() for r in members]

    def post(self):
        data = request.get_json()
        new_member = self.add_new_member(data)
        f.flash('El socio "' + new_member.name + '" fue creado con éxito')
        return new_member.serialize()

    @staticmethod
    def get_all_members():
        query = session.query(models.Member).filter(models.Member.deleted_at == None)
        return query.all()

    @staticmethod
    def add_new_member(data):
        member = models.Member(
            name=data.get('name'),
            address=data.get('address'),
            telephone=data.get('telephone'),
            plan_id=data.get('plan_id'),
            member_number=data.get('member_number')
        )

        session.add(member)
        session.commit()

        return member
