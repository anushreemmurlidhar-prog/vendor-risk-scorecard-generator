import os
from flask import Blueprint, current_app, g, jsonify, request
from services.groq_client import GroqClient


generate_report_bp = Blueprint("generate_report", __name__)


def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "generate_report.txt")
    with open(prompt_path, "r", encoding="utf-8") as handle:
        return handle.read()


@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    payload = getattr(g, "sanitized_json", None)
    if payload is None:
        payload = request.get_json(silent=True) or {}

    vendor_name = payload.get("vendor", "").strip()
    assessment = payload.get("assessment", "").strip()

    if not vendor_name or not assessment:
        return jsonify({"error": "vendor and assessment fields are required."}), 400

    prompt_template = load_prompt()
    prompt = prompt_template.format(vendor=vendor_name, assessment=assessment)
    try:
        groq_client = GroqClient()
        report_text = groq_client.generate_report(prompt)
    except Exception as exc:
        current_app.logger.error("Failed to generate report: %s", exc)
        return (
            jsonify(
                {
                    "error": "AI service unavailable. Please retry later.",
                    "details": str(exc),
                }
            ),
            502,
        )

    return jsonify(
        {
            "vendor": vendor_name,
            "generated_report": report_text,
            "source": "groq",
        }
    )
