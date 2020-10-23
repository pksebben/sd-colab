import os
import unittest
import datetime
import time

import flask
from flask import session
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base

import app as app
import db, models, fixtures

def setUpModule():
    app.init()
    db.init(app.app)

class StartTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        fixtures.gogogadget()
        cls.tester = app.app.test_client()
        
    def setUp(self):
        self.templates = []
        flask.template_rendered.connect(self._record_template, app.app)

    def tearDown(self):
        flask.template_rendered.disconnect(self._record_template, app.app)

    def _record_template(self, sender, template, context, **extra):
        self.templates.append(template)
        self.context = context

    """
    BEGIN TESTS
    """
    
    # api.create_user()
    
    def test_create_user_success_response(self):
        res = self.tester.post('/create_user', data=dict(
            email= "sam@gmail.com",
            name="sam",
            password = "pass",
            admin = False
        ))
        self.assertEqual(res.status_code, 200)

    def test_create_user_success_exists(self):
        res = self.tester.post('/create_user', data=dict(
            email = "bob@gmail.com",
            name = "bob",
            password = "pass",
            admin = False
        ))
        bob = db.db.session.query(models.Member).filter(models.Member.email == "bob@gmail.com").first()
        self.assertTrue(bob)

    def test_create_user_exists(self):                    
        res = self.tester.post('/create_user', data=dict(
            email="tom@gmail.com",
            password="pass",
            admin=False
        ))
        self.assertEqual(res.status_code, 400)

    def test_user_update(self):
        res = self.tester.post('/edit/user/1', data=dict(
            email="bill@gmail.com",
            name="bob"
        ))
        self.assertEqual(res.json['name'], "bob")

    def test_partial_user_update(self):
        res = self.tester.post('/edit/user/2', data=dict(
            name="tom"
        ))
        self.assertEqual(res.json['name'], "tom")

    def test_create_machine(self):
        res = self.tester.post('/create_machine', data=dict(
            name='the buzzsawinator'
        ))
        self.assertEqual(res.status_code, 200)

    def test_request_reservation(self):
        res = self.tester.post('/reserve', data=dict(
            date = "2021-01-01",
            start = "12:00:00",
            end = "14:00:00",
            machine_id = 1,
            member_id = 1
        ))
        self.assertEqual(res.status_code, 200)
        
    def test_reservation_unavailable(self):
        setup = self.tester.post('/reserve', data=dict(
            date = "2021-02-01",
            start = "12:00:00",
            end = "14:00:00",
            machine_id = 1,
            member_id = 1
        ))
        res = self.tester.post('/reserve', data=dict(
            date = "2021-02-01",
            start = "12:00:00",
            end = "14:00:00",
            machine_id = 1,
            member_id = 2
        ))
        self.assertEqual(res.status_code, 409)

    def test_adjacent_reservations(self):
        setup = self.tester.post('/reserve', data=dict(
            date = "2021-03-01",
            start = "12:00:00",
            end = "14:00:00",
            machine_id = 1,
            member_id = 3
        ))
        res = self.tester.post('/reserve', data=dict(
            date = "2021-03-01",
            start = "14:00:00",
            end = "16:00:00",
            machine_id = 1,
            member_id = 4
        ))
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
