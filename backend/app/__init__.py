from flask import Flask
from .config import Config
from .database import init_db
from flasgger import Swagger
from .auth.routes import auth_bp
from .tasks.routes import tasks_bp

def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config)

    if testing:
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = app.config['MONGO_TEST_URI']

    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "securityDefinitions": {
            "APIKeyHeader": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Token. Format: Bearer {token}"
            }
        }
    }
    Swagger(app, config=swagger_config)

    # Initialize Database
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "The requested resource was not found on this server"}, 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return {"error": "The HTTP method is not allowed for this endpoint"}, 405

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "An unexpected internal server error occurred"}, 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        # Log the error if needed
        return {"error": str(error)}, 500

    @app.route('/')
    def index():
        return {"message": "Welcome to the Multi-tenant Task API"}, 200

    return app
