"""Mini-VulnFinBot application factory."""

from flask import Flask

from app.routes import register_routes


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    register_routes(app)
    return app


app = create_app()
