from flask import Flask
from controller.config import Config


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	from controller.gateway.routes import controllerBlueprint

	app.register_blueprint(controllerBlueprint)

	return app