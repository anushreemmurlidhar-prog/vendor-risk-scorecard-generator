# AI Service Security Review

## Threats and Mitigations

1. Prompt injection
   - Detects suspicious phrases like "ignore previous", "drop table", and "<script>".
   - Rejects requests containing injected control sequences with HTTP 400.

2. Rate abuse
   - Uses `Flask-Limiter` to enforce `30 requests per minute` per client IP.
   - Protects the Groq API and prevents abusive traffic.

3. API key exposure
   - Keeps `GROQ_API_KEY` in environment variables only.
   - No hard-coded credentials in source code.

4. Malformed JSON and invalid input
   - Rejects missing required fields with clear 400 responses.
   - Sanitizes string values and strips HTML tags.

5. Downstream AI failure
   - Uses 3 retry attempts with exponential backoff for Groq requests.
   - Returns a 502 response when the Groq service is unavailable.

## Security Tests

- Empty input
  - POST `/api/generate-report` with `{}` returns 400.

- Prompt injection
  - POST `/api/generate-report` with `assessment` containing `ignore previous instructions` returns 400.

- SQL injection pattern
  - Any request containing `drop table users` or similar payload is rejected as suspicious.

- HTML content blocking
  - Requests with `<script>alert(1)</script>` are sanitized and rejected when injection patterns are detected.

- Rate limit enforcement
  - More than 30 requests per minute from one IP returns 429.
