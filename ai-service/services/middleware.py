import re
from flask import g, jsonify, request
from werkzeug.exceptions import BadRequest

HTML_TAG_RE = re.compile(r"<[^>]+>")
INJECTION_PATTERNS = [
    r"ignore previous",
    r"disregard all previous",
    r"delete\s+database",
    r"drop\s+table",
    r"shutdown",
    r"sandbox",
    r"javascript:",
    r"<script>",
    r"eval\(",
    r"/dev/shm",
]


def strip_html(value: str) -> str:
    return HTML_TAG_RE.sub("", value)


def is_prompt_injection(value: str) -> bool:
    normalized = value.lower()
    return any(re.search(pattern, normalized) for pattern in INJECTION_PATTERNS)


def sanitize_payload(payload):
    if isinstance(payload, str):
        stripped = strip_html(payload).strip()
        if is_prompt_injection(stripped):
            raise BadRequest(
                description="Prompt injection detected in request body."
            )
        return stripped

    if isinstance(payload, dict):
        return {key: sanitize_payload(value) for key, value in payload.items()}

    if isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]

    return payload


def sanitize_request():
    if request.method in ("POST", "PUT", "PATCH") and request.is_json:
        payload = request.get_json(silent=True)
        if payload is None:
            return
        try:
            g.sanitized_json = sanitize_payload(payload)
        except BadRequest as exc:
            response = jsonify({"error": str(exc.description)})
            response.status_code = 400
            return response
