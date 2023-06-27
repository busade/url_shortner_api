import unittest
from .. import create_app
from ..utils import db
from ..config.config import config_dict
from werkzeug.security import generate_password_hash




class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def teardown(self):
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None



    def test_user_Signup(self):
        data = {
            "fullname": "test",
            "email": "test@gmail.com",
            "password_hash": "test"
        }
        response = self.client.post('/auth/signup', json=data)
        assert response.status_code == 201