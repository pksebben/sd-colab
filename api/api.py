import flask
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt

from errors import UserInputError
import db
import models

api = flask.Blueprint("api", __name__)

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
    user = db.db.session.query(models.Member).filter(models.Member.id == userid).first()
    if user is not None:
        return flask.jsonify({
            'status_code' : 200,
            "email" : user.email,
            "created" : user.created,
            "name" : user.name
        }), 200
    else:
        return flask.jsonify({
            "status_code" : 400,
            "msg": "no user with id = {} found".format(userid)
        }), 400

@api.route('/test_query_object', methods=['GET'])
def test_query():
    user = db.db.session.query(models.Member).filter(models.Member.id == 1).first()
    print('emailblerp' in dir(user))
    return user['email']

# TODO: auth
@api.route('/edit/user/<userid>', methods=['POST'])
def edit_user(userid):
    user = db.db.session.query(models.Member).filter(models.Member.id == userid).first()
    print("DIR FLASK REQUEST VALUES")
    print(flask.request.values.keys())
    user.name = flask.request.values['name'] if 'name' in flask.request.values.keys() else user.name
    user.email = flask.request.values['email'] if 'email' in flask.request.values.keys() else user.email
    db.db.session.commit()
    updated_user = db.db.session.query(models.Member).filter(models.Member.id == userid).first()
    return flask.jsonify({
        'status_code': 200,
        'msg': "user registered",
        'name' : updated_user.name,
        'email' : updated_user.email,
        'id' : updated_user.id,
        'created' : updated_user.created
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
        return flask.jsonify({'status_code': 200, 'msg': 'user %s registered on machine %s'.format()})
    except IntegrityError as e:
        raise e


@api.route('/create_machine', methods=["POST"])
def create_machine():
    pass


@api.route('/schedule_timeslot', methods=["POST"])
def schedule_timeslot():
    pass

# TODO: timeslots feel like the wrong answer.  Not flexible enough and I'll probably have to implement all sorts of hax to get them working.
@api.route('/get_calendar/<machineid>', methods=["GET"])
def get_calendar(machineid):
    timeslots = db.db.session.query(
        models.TimeSlot).filter(
        machine_id == machineid).all()
    return jsonify([timeslots.to_json() for timeslot in timeslots])
