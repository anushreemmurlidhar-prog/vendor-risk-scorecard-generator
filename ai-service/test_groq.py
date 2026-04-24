import os
from dotenv import load_dotenv
from services.groq_client import GroqClient

load_dotenv()


def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("GROQ_API_KEY is not set. Copy ai-service/.env.example to .env and add your key.")

    client = GroqClient()
    prompt = (
        "Write a short summary of vendor risk for a sample vendor. "
        "Mention confidentiality, compliance, and remediation steps."
    )

    try:
        output = client.generate_report(prompt)
        print("=== Groq response ===")
        print(output)
    except Exception as exc:
        print("Groq test failed:", exc)


if __name__ == "__main__":
    main()
