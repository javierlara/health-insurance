from flask_restful import Resource
from flask import abort, make_response, request
import api.models as models
from datetime import datetime
from api.db import db_session as session


class Plan(Resource):
    @staticmethod
    def get_plan(plan_id):
        return session.query(models.Plan).get(plan_id)

    @staticmethod
    def delete_plan(plan):
        plan.deleted_at = datetime.utcnow()
        session.commit()

    @staticmethod
    def update_plan(plan, data):
        plan.update(data)
        session.commit()

    def get(self, plan_id):
        plan = self.get_plan(plan_id)
        if plan is None:
            abort(404)
        return plan.serialize()

    def put(self, plan_id):
        plan = self.get_plan(plan_id)
        if plan is None:
            abort(404)
        data = request.get_json()
        self.update_plan(plan, data)
        return plan.serialize()

    def delete(self, plan_id):
        plan = self.get_plan(plan_id)
        if plan is None:
            abort(404)
        self.delete_plan(plan)
        return make_response()


class PlanCollection(Resource):
    def get(self):
        plans = self.get_all_plans()
        return [r.serialize() for r in plans]

    def post(self):
        data = request.get_json()
        new_plan = self.add_new_plan(data)
        return new_plan.serialize()

    @staticmethod
    def get_all_plans():
        query = session.query(models.Plan).filter(models.Plan.deleted_at == None)
        return query.all()

    @staticmethod
    def add_new_plan(data):
        plan = models.Plan(
            name=data.get('name')
        )

        session.add(plan)
        session.commit()

        return plan
