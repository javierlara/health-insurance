from flask_restful import Resource
import api.models as models
from flask_restful import reqparse
from math import radians, cos, sin, asin, sqrt

from api.db import db_session as session


def map_distance_sorted(items, lat, long):
    list = []
    for item in items:
        splited = item.location.split(',');

        item.distance = distance(float(lat), float(long), float(splited[0][1:]), float(splited[1][:-1]))
        list.append(item)

    list.sort(key=lambda item: item.distance)

    return list


def distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


class Cartilla(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('plan_id')
        parser.add_argument('speciality_id')
        parser.add_argument('lat')
        parser.add_argument('long')
        args = parser.parse_args()

        plan_id = args.get('plan_id')
        speciality_id = args.get('speciality_id')
        lat = args.get('lat')
        long = args.get('long')
        doctors = self.get_filtered_doctors(plan_id, speciality_id, lat, long)
        return [r.serialize() for r in doctors]

    @staticmethod
    def get_filtered_doctors(plan_id, speciality_id, lat, long):
        query = session.query(models.Doctor).filter(models.Doctor.deleted_at == None)
        if speciality_id:
            query = query.filter(models.Doctor.specialities.any(id=speciality_id))
        if plan_id:
            query = query.filter(models.Doctor.plans.any(id=plan_id))
        results = query.all()
        if long and lat:
            results = map_distance_sorted(results, lat, long)

        return results