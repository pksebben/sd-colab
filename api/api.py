import flask
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt

from errors import UserInputError
import db
import models

api = flask.Blueprint("api", __name__)

# sanitize input?  Do we even need to?
# def scrubvals(values):
#     def _scrub(value):
#         if type(value) == str:
#             return value.encode('utf-8', 'ignore')
#         else:
#             return value
#     scrubbed = [value.encode('utf-8', 'ignore') for value in values if type(value) == str]
#     return scrubbed

@api.route('/register_user', methods=["POST"])
def register_user():
    db.db.session.add(
        models.Member(
            email=flask.request.values["email"],
            passhash=bcrypt.hash(flask.request.values['password']),
            admin=False))
    try:
        db.db.session.commit()
        return flask.jsonify({'status_code':200, 'msg':"user registered"}), 200
    except IntegrityError:
        return flask.jsonify({'status_code':400, 'msg':'duplicate email error'}), 400


@api.route('/certify')
def certify():
    db.db.session.add(models.MemberToMachine(
        member_id = flask.request.values['memberid'],
        machine_id = flask.request.values['machineid'],
        instructor = flask.request.values['instructor']
    ))
    try:
        db.db.session.commit()
        return flask.jsonify({'status_code':200, 'msg':'user %s registered on machine %s'.format()})

@api.route('/create_machine', methods=["POST"])
def create_machine():
    pass


@api.route('/schedule_timeslot', methods=["POST"])
def schedule_timeslot():
    pass


@api.route('/get_calendar/<machineid>', methods=["GET"])
def get_calendar(machineid):
    timeslots = db.db.session.query(
        models.TimeSlot).filter(
        machine_id == machineid).all()
    return jsonify([timeslots.to_json() for timeslot in timeslots])
