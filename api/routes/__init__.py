from flask.ext.restful import Api
from api import app
from api.routes.login import login_required
from api.routes.resources.appointment import Appointment
from .resources.schedule import Schedule
from .resources.health_center import HealthCenter, HealthCenterCollection
from .resources.news import NewsCollection, News
from .resources.plan import Plan, PlanCollection
from .resources.speciality import Speciality, SpecialityCollection
from .resources.doctor import Doctor, DoctorCollection
from .resources.member import Member, MemberCollection
from .resources.cartilla import Cartilla
from flask import render_template, jsonify


api = Api(app)

api.add_resource(HealthCenter, '/api/health_centers/<string:health_center_id>')
api.add_resource(HealthCenterCollection, '/api/health_centers')
api.add_resource(News, '/api/news/<string:news_id>')
api.add_resource(NewsCollection, '/api/news')
api.add_resource(Plan, '/api/plans/<string:plan_id>')
api.add_resource(PlanCollection, '/api/plans')
api.add_resource(Speciality, '/api/specialities/<string:speciality_id>')
api.add_resource(SpecialityCollection, '/api/specialities')
api.add_resource(Doctor, '/api/doctors/<string:doctor_id>')
api.add_resource(DoctorCollection, '/api/doctors')
api.add_resource(Cartilla, '/api/cartilla')
api.add_resource(Member, '/api/members/<string:member_id>')
api.add_resource(MemberCollection, '/api/members')


#SCHEDULES

@app.route('/api/doctors/<int:doctor_id>/schedule/<int:miliseconds>', methods=['GET'])
def get_schedule(doctor_id, miliseconds):
    schedule = Schedule()
    return jsonify(schedule.get(doctor_id, miliseconds))

@app.route('/api/doctors/<int:doctor_id>/schedule', methods=['POST'])
def post_schedule(doctor_id):
    schedule = Schedule()
    return jsonify(schedule.post(doctor_id))

@app.route('/api/doctors/<int:doctor_id>/schedule', methods=['PUT'])
def put_schedule(doctor_id):
    schedule = Schedule()
    return jsonify(schedule.put(doctor_id))

@app.route('/api/doctors/<int:doctor_id>/days/<int:month>/<int:year>', methods=['GET'])
def get_schedule_days_by_month_and_year(doctor_id, month, year):
    schedule = Schedule()
    a = schedule.getDays(doctor_id, month, year)
    return jsonify(a)

@app.route('/api/doctors/<int:doctor_id>/schedule/<int:month>/<int:year>', methods=['GET'])
def get_schedule_schedule_by_month_and_year(doctor_id, month, year):
    schedule = Schedule()
    a = schedule.getMonthSchedule(doctor_id, month, year)
    return jsonify(a)

#APPOINTMENTS

@app.route('/api/appointment', methods=['POST'])
# Recibe doctor_id, member_id, start
def post_appointment():
    appointment = Appointment()
    return jsonify(appointment.post())




@app.route('/health_centers/new', methods=['GET'])
@login_required
def new_center():
    plans = PlanCollection.get_all_plans()
    return render_template('centers/newCenter.html', plans=plans)


@app.route('/health_centers', methods=['GET'])
@login_required
def health_centers():
    centers = HealthCenterCollection.get_all_health_centers()
    return render_template('centers/listCenters.html', centers=centers)


@app.route('/health_centers/edit/<int:center_id>', methods=['GET'])
@login_required
def edit_center(center_id):
    center = HealthCenter.get_health_center(center_id)
    plans = PlanCollection.get_all_plans()
    center_plan_ids = list(map(lambda x: x.id, center.plans))
    return render_template('centers/newCenter.html',
                           center=center,
                           plans=plans,
                           center_plan_ids=center_plan_ids
                           )


@app.route('/news/new', methods=['GET'])
@login_required
def new_news():
    return render_template('news/newNews.html')


@app.route('/news', methods=['GET'])
@login_required
def newses():
    newses = NewsCollection.get_all_news()
    return render_template('news/listNews.html', newses=newses)


@app.route('/news/edit/<int:news_id>', methods=['GET'])
@login_required
def edit_news(news_id):
    news = News.get_news(news_id)
    return render_template('news/newNews.html', news=news)


@app.route('/plans/new', methods=['GET'])
@login_required
def new_plan():
    return render_template('plans/newPlan.html')


@app.route('/plans', methods=['GET'])
@login_required
def plans():
    plans = PlanCollection.get_all_plans()
    return render_template('plans/listPlans.html', plans=plans)


@app.route('/plans/edit/<int:plan_id>', methods=['GET'])
@login_required
def edit_plan(plan_id):
    plan = Plan.get_plan(plan_id)
    return render_template('plans/newPlan.html', plan=plan)


@app.route('/specialities/new', methods=['GET'])
@login_required
def new_speciality():
    return render_template('specialities/newSpeciality.html')


@app.route('/specialities', methods=['GET'])
@login_required
def specialities():
    specialities = SpecialityCollection.get_all_specialities()
    return render_template('specialities/listSpecialities.html', specialities=specialities)


@app.route('/specialities/edit/<int:speciality_id>', methods=['GET'])
@login_required
def edit_speciality(speciality_id):
    speciality = Speciality.get_speciality(speciality_id)
    return render_template('specialities/newSpeciality.html', speciality=speciality)


@app.route('/doctors/new', methods=['GET'])
@login_required
def new_doctor():
    plans = PlanCollection.get_all_plans()
    specialities = SpecialityCollection.get_all_specialities()
    return render_template('doctors/newDoctor.html', plans=plans, specialities=specialities)


@app.route('/doctors', methods=['GET'])
@login_required
def doctors():
    doctors = DoctorCollection.get_all_doctors()
    return render_template('doctors/listDoctors.html', doctors=doctors)


@app.route('/doctors/edit/<int:doctor_id>', methods=['GET'])
@login_required
def edit_doctor(doctor_id):
    doctor = Doctor.get_doctor(doctor_id)
    plans = PlanCollection.get_all_plans()
    doctor_plan_ids = list(map(lambda x: x.id, doctor.plans))
    specialities = SpecialityCollection.get_all_specialities()
    doctor_speciality_ids = list(map(lambda x: x.id, doctor.specialities))
    return render_template('doctors/newDoctor.html',
                           doctor=doctor,
                           plans=plans,
                           doctor_plan_ids=doctor_plan_ids,
                           specialities=specialities,
                           doctor_speciality_ids=doctor_speciality_ids
                           )


@app.route('/members/new', methods=['GET'])
@login_required
def new_member():
    plans = PlanCollection.get_all_plans()
    return render_template('members/newMember.html', plans=plans)


@app.route('/members', methods=['GET'])
@login_required
def members():
    members = MemberCollection.get_all_members()
    return render_template('members/listMembers.html', members=members)


@app.route('/members/edit/<int:member_id>', methods=['GET'])
@login_required
def edit_member(member_id):
    member = Member.get_member(member_id)
    plans = PlanCollection.get_all_plans()
    return render_template('members/newMember.html',
                           member=member,
                           plans=plans,
                           )


@app.route('/doctors/<int:doctor_id>/schedule', methods=['GET'])
@login_required
def edit_schedule(doctor_id):
    doctor = Doctor.get_doctor(doctor_id)
    return render_template('doctors/editSchedule.html',
                           doctor=doctor
                           )



@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')


