from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "messages": error.messages
        }), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "message": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error)
        }), 500

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.sort_keys = False

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .routes.messages import messages_bp
    app.register_blueprint(messages_bp, url_prefix="/messages")
    from app.routes.comments import comments_bp
    app.register_blueprint(comments_bp)
    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")
    register_error_handlers(app)

    return app