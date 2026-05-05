# AI Service for Tool-93

## Setup

1. Install dependencies: pip install -r requirements.txt

2. Set environment: copy .env.example to .env, add GROQ_API_KEY

3. Run: python app.py

## Environment Variables

- GROQ_API_KEY: Your Groq API key

## Run Instructions

- Local: python app.py

- Docker: docker build -t ai-service . && docker run -p 5000:5000 ai-service

## API Reference

### POST /describe

Input: {"vendor_name": string, "risk_factors": string}

Output: {"description": string, "generated_at": string}

### POST /recommend

Input: {"vendor_name": string, "risk_factors": string}

Output: {"recommendations": array, "generated_at": string}

### POST /generate-report

Input: {"vendor_name": string, "risk_factors": string}

Output: {"report": object, "generated_at": string}

### GET /health

Output: {"status": "healthy", "model": string, "uptime": string, "avg_response_time": string}