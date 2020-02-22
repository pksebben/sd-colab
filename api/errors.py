from flask import jsonify

"""
API exceptions are to be defined in here
these exceptions should have some logging, when complete.
"""

class UserInputError(Exception):
    status_code = 400

    def __init_(self, msg, status_code=None, payload=None):
        Exception.__init__(self)
        self.msg = msg
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.msg
        return rv

class SchedulingError(Exception):
    status_code = 400

    def __init_(self, msg, status_code=None, payload=None):
        Exception.__init__(self)
        self.msg = msg
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.msg
        return rv
