import flask
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
import datetime
import time

from errors import UserInputError
import db
import models

api = flask.Blueprint("api", __name__)

TIME_FORMAT = "%H:%M:%S"


@api.route('/api_test', methods=['GET'])
def test_api_available():
    return "api routes are registered and available"

# TODO: auth


@api.route('/create_user', methods=["POST"])
def create_user():
    db.db.session.add(
        models.Member(
            email=flask.request.values["email"],
            passhash=bcrypt.hash(flask.request.values['password']),
            name=flask.request.values['name'],
            admin=False))
    try:
        db.db.session.commit()
        return flask.jsonify(
            {'status_code': 200, 'msg': "user registered"}), 200
    except IntegrityError:
        return flask.jsonify(
            {'status_code': 400, 'msg': 'duplicate email error'}), 400


@api.route('/user/<userid>', methods=['GET'])
def get_user(userid):
    user = db.db.session.query(
        models.Member).filter(
        models.Member.id == userid).first()
    if user is not None:
        return flask.jsonify({
            'status_code': 200,
            "email": user.email,
            "created": user.created,
            "name": user.name
        }), 200
    else:
        return flask.jsonify({
            "status_code": 400,
            "msg": "no user with id = {} found".format(userid)
        }), 400

# TODO: Delete me for prod


@api.route('/test_query_object', methods=['GET'])
def test_query():
    user = db.db.session.query(
        models.Member).filter(
        models.Member.id == 1).first()
    print('emailblerp' in dir(user))
    return user['email']

# TODO: auth


@api.route('/edit/user/<userid>', methods=['POST'])
def edit_user(userid):
    user = db.db.session.query(
        models.Member).filter(
        models.Member.id == userid).first()
    user.name = flask.request.values['name'] if 'name' in flask.request.values.keys(
    ) else user.name
    user.email = flask.request.values['email'] if 'email' in flask.request.values.keys(
    ) else user.email
    db.db.session.commit()
    updated_user = db.db.session.query(
        models.Member).filter(
        models.Member.id == userid).first()
    # TODO: is there a prettier way to serialize the object into the response?
    return flask.jsonify({
        'status_code': 200,
        'msg': "user registered",
        'name': updated_user.name,
        'email': updated_user.email,
        'id': updated_user.id,
        'created': updated_user.created
    }), 200


@api.route('/certify')
def certify():
    db.db.session.add(models.MemberToMachine(
        member_id=flask.request.values['memberid'],
        machine_id=flask.request.values['machineid'],
        instructor=flask.request.values['instructor']
    ))
    try:
        db.db.session.commit()
        return flask.jsonify(
            {'status_code': 200, 'msg': 'user %s registered on machine %s'.format()})
    except IntegrityError as e:
        raise e


@api.route('/create_machine', methods=["POST"])
def create_machine():
    db.db.session.add(models.Machine(
        name=flask.request.values['name']
    ))
    db.db.session.commit()
    machine = db.db.session.query(
        models.Machine).order_by(
        models.Machine.id.desc()).first()
    return flask.jsonify(
        {'status_code': 200, 'msg': 'machine {} added'.format(machine.name)})


@api.route('/schedule_timeslot', methods=["POST"])
def schedule_timeslot():
    pass

# TODO: timeslots feel like the wrong answer.  Not flexible enough and
# I'll probably have to implement all sorts of hax to get them working.


@api.route('/get_calendar/<machineid>', methods=["GET"])
def get_calendar(machineid):
    timeslots = db.db.session.query(
        models.TimeSlot).filter(
        machine_id == machineid).all()
    return jsonify([timeslots.to_json() for timeslot in timeslots])


@api.route('/reserve', methods=['POST'])
def request_reservation():
    desired_date = datetime.date.fromisoformat(flask.request.values['date'])
    desired_start = flask.request.values['start']
    desired_end = flask.request.values['end']
    machine = db.db.session.query(models.Machine).filter(
        models.Machine.id == flask.request.values['machine_id']).one()
    member = db.db.session.query(models.Member).filter(
        models.Member.id == flask.request.values['member_id']).one()
    reservations = db.db.session.query(
        models.Reservation).filter(
        models.Reservation.date == desired_date).filter(
            models.Reservation.machine_id == machine.id)

    if reservations is not None:
        for reservation in reservations:
            if (time.strptime(reservation.end, TIME_FORMAT) <= time.strptime(desired_start, TIME_FORMAT)
                    or time.strptime(reservation.start, TIME_FORMAT) >= time.strptime(desired_end, TIME_FORMAT)):
                pass
            else:
                # maybe also return the calendar
                return flask.jsonify({
                    msg: "sorry, but {} has a booking in that time slot already".format(reservation.member.name),
                    status_code: 409
                }), 409 # TODO: input correct return code

    db.db.session.add(models.Reservation(
        date=desired_date,
        start=desired_start,
        end=desired_end,
        machine_id=machine.id,
        member_id=member.id
    ))
    db.db.session.commit()
    return flask.jsonify({
        'msg': 'congratulations! {} is booked on the {} for {} - {} on {}.  Don\'t be late!'.format(member.name, machine.name, desired_start, desired_end, desired_date),
        'status_code': 200
    }), 200


def get_reservations(date, machineid):
    reservations = db.db.session.query(
        models.Reservation).filter(
        models.Reservation.machine_id == machineid).filter(
            models.Reservation.date == date)
    # TODO: serialization
    return reservations
