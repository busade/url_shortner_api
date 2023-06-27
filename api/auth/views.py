from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from http import HTTPStatus
from werkzeug.exceptions import Conflict,  BadRequest




auth_namespace = Namespace('auth', description='Authentication related operations')
auth_model = auth_namespace.model('User', {
    'fullname': fields.String(required=True, description='User fullname'),
    'email': fields.String(required=True, description='User email address'),
    'password_hash': fields.String(required=True, description='User password'),
    'is_active': fields.Boolean(required=True, description='User status'),
    'created_at': fields.DateTime(required=True, description='User created date'),

})

login_model = auth_namespace.model('Login', 
                                   {
                                       'email': fields.String(required=True, description='User email address'),
                                       'password_hash': fields.String(required=True, description='User password'),
                                   })



@auth_namespace.route('/signup')
class Signup(Resource):
    @auth_namespace.expect(auth_model)
    @auth_namespace.marshal_with(auth_model)
    def post(self):
        '''User Signup'''

        data = request.get_json()
        try:
            new_user= Users(
                fullname=data.get('fullname'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password_hash'))
            )
            new_user.save()
            return new_user, HTTPStatus.CREATED
        except Exception as e:
            raise Conflict (f"User with {data.get('email')} exists")


@auth_namespace.route('/')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
      '''Generate Jwt Token'''
      data = request.get_json()
      email = data.get('email')
      password = data.get('password_hash')
      user = Users.query.filter_by(email=email).first()

      if user is not None and check_password_hash(user.password_hash, password):
          access_token = create_access_token(identity=user.id)
          refresh_token = create_refresh_token(identity=user.id)
          response = {
              'access_token': access_token,
                'refresh_token': refresh_token
            }
          return response, HTTPStatus.OK
      raise BadRequest('Invalid credentials')



@auth_namespace.route('/refresh') 
class Refresh(Resource):
    @jwt_required(refresh=True)
    def get(self):
        '''Refresh Jwt Token'''
        username= get_jwt_identity()
        access_token = create_access_token(identity=username)
        return {"access_token":access_token}, HTTPStatus.OK