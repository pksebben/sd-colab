import os
import unittest

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
    
    # api.register_user()
    
    def test_register_user_success_response(self):
        res = self.tester.post('/register_user', data=dict(
            email= "sam@gmail.com",
            password = "pass",
            admin = False
        ))
        self.assertEqual(res.status_code, 200)

    def test_register_user_success_exists(self):
        res = self.tester.post('/register_user', data=dict(
            email = "bob@gmail.com",
            password = "pass",
            admin = False
        ))
        bob = db.db.session.query(models.Member).filter(models.Member.email == "bob@gmail.com").first()
        self.assertTrue(bob)

    def test_register_user_exists(self):                    
        res = self.tester.post('/register_user', data=dict(
            email="tom@gmail.com",
            password="pass",
            admin=False
        ))
        self.assertEqual(res.status_code, 400)

if __name__ == "__main__":
    unittest.main()
