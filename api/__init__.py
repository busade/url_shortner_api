from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .links.views import links_namespace
from .config.config import config_dict
from .utils import db
from .models.users import Users
from .models.urls import Links, Analysis
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.exceptions import NotFound, MethodNotAllowed



def create_app(config=config_dict['prod']):
    app = Flask(__name__)
    app.config.from_object(config)
    api=Api(app,
            title="url Shortner API",
            version="1.0",
            description="A simple url shortner API"
            )
    CORS(app)
    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(links_namespace, path='/links')
    

    @app.errorhandler(NotFound)
    def not_found(error):    
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': 'Method not allowed'}, 405
    
    
    @app.shell_context_processor
    def make_shell_context():
        db.create_all()
        return {
            'db':db,
            'Users':Users,
            'Links':Links,
        }
    return app