import os
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from services.middleware import sanitize_request
from routes.generate_report import generate_report_bp
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    Limiter(app, key_func=get_remote_address, default_limits=["30 per minute"])
    app.register_blueprint(generate_report_bp, url_prefix="/api")

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(status="ok", version="1.0.0")

    app.before_request(sanitize_request)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
