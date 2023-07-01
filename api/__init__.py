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
from flask_swagger_ui import get_swaggerui_blueprint



def create_app(config=config_dict['prod']):
    app = Flask(__name__)
    app.config.from_object(config)
    authorizations = {
        "Bearer Auth": {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'Description':"add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }

    api=Api(app,
            title="url Shortner API",
            version="1.0",
            description="A simple url shortner API",
            authorizations=authorizations,
            security='Bearer Auth'

            )
    CORS(app, origins=['http://127.0.0.1:5500'])
    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(links_namespace, path='/links')
    
    SWAGGER_URL = '/swagger'
    Api_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        Api_URL,
        config={"app_name": "url Shortner API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.errorhandler(NotFound)
    def not_found(error):    
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': 'Method not allowed'}, 405
    
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'Users':Users,
            'Links':Links,
        }
    return app