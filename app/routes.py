"""HTTP routes and the deterministic mock assistant."""

from flask import jsonify, request

MAX_MESSAGE_LENGTH = 2000
MOCK_RESPONSE = "You can start by tracking your income and expenses."


def generate_response(_message):
    """Return a fixed tip; user text is never interpreted or sent elsewhere."""
    return MOCK_RESPONSE


def register_routes(app):
    @app.get("/health")
    def health():
        return jsonify(status="healthy")

    @app.post("/api/chat")
    def chat():
        if not request.is_json:
            return jsonify(error="Content-Type must be application/json"), 415
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="Request body must be a JSON object"), 400
        message = payload.get("message")
        if not isinstance(message, str) or not message.strip():
            return jsonify(error="'message' must be a non-empty string"), 400
        if len(message) > MAX_MESSAGE_LENGTH:
            return jsonify(error="'message' must be at most 2000 characters"), 400

        response = generate_response(message)
        if not isinstance(response, str) or not response.strip() or len(response) > 2000:
            return jsonify(error="Assistant response unavailable"), 502
        return jsonify(response=response)
