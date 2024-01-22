from flask import Flask

from api.controller import companion_plant_controller


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(companion_plant_controller, url_prefix='/companions')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)