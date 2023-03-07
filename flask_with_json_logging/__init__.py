from flask import Flask

from flask_with_json_logging.api import api as api_bp
from flask_with_json_logging.config import config


def create_app(config_name='default'):
    app = Flask(__name__)
    app_config = config[config_name]
    app.config.from_object(app_config)
    app_config.init_app(app)

    app.register_blueprint(api_bp)

    return app
