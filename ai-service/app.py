from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import bleach
import re
import os
from services.groq_client import GroqClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
limiter = Limiter(app)

groq_client = GroqClient()

# Middleware for input sanitisation
@app.before_request
def sanitize_input():
    if request.method in ['POST', 'PUT', 'PATCH'] and request.is_json:
        data = request.get_json()
        for key, value in data.items():
            if isinstance(value, str):
                # Strip HTML
                data[key] = bleach.clean(value, tags=[], strip=True)
                # Detect prompt injection
                if detect_prompt_injection(data[key]):
                    return jsonify({"error": "Invalid input"}), 400
        # For simplicity, assume data is used directly in routes

def detect_prompt_injection(text):
    # Simple detection
    patterns = [
        r'ignore.*previous',
        r'forget.*instructions',
        r'new.*instructions',
        r'system.*prompt',
        r'you.*are.*now',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# Fallback responses when AI is unavailable
def fallback_description(vendor_name, risk_factors):
    return (
        f"{vendor_name} appears to have elevated risk due to {risk_factors}. "
        "Review financial controls, compliance posture, and third-party oversight immediately."
    )

def fallback_recommendations(vendor_name, risk_factors):
    return [
        {
            "action_type": "Monitor",
            "description": f"Monitor {vendor_name}'s remediation progress for {risk_factors}.",
            "priority": "high"
        },
        {
            "action_type": "Audit",
            "description": f"Perform an audit of {vendor_name}'s control environment.",
            "priority": "medium"
        },
        {
            "action_type": "Escalate",
            "description": f"Escalate the risk findings for {vendor_name} to senior management.",
            "priority": "low"
        }
    ]

def fallback_report(vendor_name, risk_factors):
    return {
        "title": f"Risk Assessment Report for {vendor_name}",
        "summary": f"{vendor_name} has been flagged for {risk_factors}. Immediate review is recommended.",
        "overview": f"The vendor was evaluated on the supplied risk factors: {risk_factors}.",
        "key_items": [
            f"Risk factors identified: {risk_factors}",
            "Control gaps need investigation",
            "Follow-up actions should be tracked"
        ],
        "recommendations": fallback_recommendations(vendor_name, risk_factors)
    }

# Routes
@app.route('/describe', methods=['POST'])
@limiter.limit("30 per minute")
def describe():
    data = request.get_json()
    vendor_name = data.get('vendor_name')
    risk_factors = data.get('risk_factors')
    # Load prompt
    with open('prompts/describe_prompt.txt', 'r') as f:
        prompt = f.read()
    prompt = prompt.format(vendor_name=vendor_name, risk_factors=risk_factors)
    try:
        response = groq_client.call_groq(prompt)
        return jsonify({
            "description": response,
            "generated_at": datetime.utcnow().isoformat()
        })
    except Exception:
        return jsonify({
            "description": fallback_description(vendor_name, risk_factors),
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": True
        }), 200

@app.route('/recommend', methods=['POST'])
@limiter.limit("30 per minute")
def recommend():
    data = request.get_json()
    vendor_name = data.get('vendor_name')
    risk_factors = data.get('risk_factors')
    with open('prompts/recommend_prompt.txt', 'r') as f:
        prompt = f.read()
    prompt = prompt.format(vendor_name=vendor_name, risk_factors=risk_factors)
    try:
        response = groq_client.call_groq(prompt)
        # Assume response is JSON string
        import json
        recommendations = json.loads(response)
        return jsonify({
            "recommendations": recommendations,
            "generated_at": datetime.utcnow().isoformat()
        })
    except Exception:
        return jsonify({
            "recommendations": fallback_recommendations(vendor_name, risk_factors),
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": True
        }), 200

@app.route('/generate-report', methods=['POST'])
@limiter.limit("30 per minute")
def generate_report():
    data = request.get_json()
    vendor_name = data.get('vendor_name')
    risk_factors = data.get('risk_factors')
    with open('prompts/generate_report_prompt.txt', 'r') as f:
        prompt = f.read()
    prompt = prompt.format(vendor_name=vendor_name, risk_factors=risk_factors)
    try:
        response = groq_client.call_groq(prompt)
        import json
        report = json.loads(response)
        return jsonify({
            "report": report,
            "generated_at": datetime.utcnow().isoformat()
        })
    except Exception:
        return jsonify({
            "report": fallback_report(vendor_name, risk_factors),
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": True
        }), 200

@app.route('/health', methods=['GET'])
def health():
    # Simple health
    return jsonify({
        "status": "healthy",
        "model": "llama3-70b-8192",
        "uptime": "running",
        "avg_response_time": "2s"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)