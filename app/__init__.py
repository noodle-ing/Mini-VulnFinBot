"""Mini-VulnFinBot application factory."""

from flask import Flask

from app.routes import register_routes


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    register_routes(app)

    @app.after_request
    def add_security_headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
        )
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    return app


app = create_app()
