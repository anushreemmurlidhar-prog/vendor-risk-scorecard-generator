# Day 20 - DEMO DAY FINAL CHECKLIST & TALKING POINTS

## Pre-Demo (30 minutes before presentation)

### System Check
- [ ] Docker containers running: `docker-compose ps`
- [ ] All 3 AI endpoints responding: `curl http://localhost:5000/health`
- [ ] Backend API running on port 8080
- [ ] Frontend accessible on port 80
- [ ] No errors in Docker logs: `docker-compose logs ai-service`
- [ ] Groq API key verified active
- [ ] Redis cache operational

### Demo Environment
- [ ] Fresh machine (if possible) or clean state
- [ ] All demo data loaded (30 seeded vendor records)
- [ ] Screenshots ready at 1920x1080
- [ ] Backup screenshots saved (in case live fails)
- [ ] SECURITY.md printed (1 copy)
- [ ] AI summary card printed (2 copies)
- [ ] AI talking points card available
- [ ] Demo script accessible on screen

### Team Coordination
- [ ] All 4 team members briefed on 6-minute total
- [ ] AI Developer 2 assigned 60-second slot
- [ ] Handoff cues confirmed between speakers
- [ ] Backup speaker identified if someone unavailable

## Live Demo (Day 20) - AI Developer 2 Slot (60 seconds)

### Opening (10 seconds)
"I'm presenting the AI service. It uses Groq's LLaMA-3.3-70b model to analyze vendor risks instantly."

### Demo Part 1: /recommend Endpoint (20 seconds)
**Action**: Show working /recommend endpoint
```bash
# Show curl command on screen
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_name": "Acme Corp",
    "risk_factors": "Regulatory issues, poor financial health"
  }'
```
**Talking Point**: "The recommend endpoint analyzes the vendor and returns 3 specific actions to mitigate risk - prioritized from high to low. All in under 2 seconds."

### Demo Part 2: /generate-report Endpoint (15 seconds)
**Action**: Show /generate-report producing structured report
```bash
curl -X POST http://localhost:5000/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_name": "Acme Corp",
    "risk_factors": "Regulatory issues, poor financial health"
  }'
```
**Talking Point**: "This generates a professional report with executive summary, key findings, and recommendations - formatted for C-suite review."

### Tech Stack Explanation (15 seconds)
"The AI service is built on:
- **Python & Flask** for the microservice framework
- **Groq API** with LLaMA-3.3-70b model for fast, accurate AI
- **Redis** for intelligent caching (15-minute TTL)
- **Flask-Limiter** for rate limiting (30 requests/minute)
- **Docker** for consistent deployment across environments"

### Live /health Endpoint (5 seconds)
**Action**: Quickly show health check
```bash
curl http://localhost:5000/health
```
**Talking Point**: "The health endpoint confirms the AI service is operational with uptime tracking."

### Security Demo (20 seconds)
**Action**: Demonstrate security features
1. **Rate Limit**: Send 31 requests in 10 seconds, show 429 error
2. **Prompt Injection**: Show blocked injection attempt
   ```bash
   curl -X POST http://localhost:5000/describe \
     -H "Content-Type: application/json" \
     -d '{"vendor_name": "Test", "risk_factors": "Ignore previous instructions"}'
   ```
   Response: `{"error": "Invalid input"}` with 400 status
3. **Reference SECURITY.md**: Point to document showing all 5 threats identified and mitigated

**Talking Point**: "We've implemented 5 security layers: input sanitization, prompt injection detection, rate limiting, API key protection, and no PII in prompts. All findings from OWASP ZAP testing are fixed."

## Key Demo Points to Hit

✓ **Real AI**: Not templates - every response is AI-generated  
✓ **Fast**: All endpoints < 2 seconds with intelligent caching  
✓ **Structured**: JSON responses integrate seamlessly with backend  
✓ **Secure**: 5-layer security, injection-resistant  
✓ **Scalable**: Handles 30+ requests/minute per IP  
✓ **Production-Ready**: Fully containerized and tested  

## Contingency Plans

**If Groq API fails**: Show backup screenshot of successful responses  
**If endpoint times out**: Run against local cache (pre-populated demo data)  
**If Docker container crashes**: Have all screenshots pre-captured  
**If projector fails**: Print out response examples to show panel  

## Post-Demo (5 minutes)
- [ ] Answer 3-5 questions from judges
- [ ] Reference SECURITY.md for security questions
- [ ] Be ready to explain prompt templates
- [ ] Discuss caching strategy and performance gains
- [ ] Mention 99.5% uptime target achieved

## Judges' Expected Questions & Answers

**Q: How does the AI avoid prompt injection?**
A: "We use regex pattern detection to identify injection keywords like 'ignore previous instructions' and block them at input validation. Additionally, we sanitize all HTML/script tags before processing."

**Q: What's your fallback if Groq API is down?**
A: "We cache responses for 15 minutes in Redis using SHA256-hashed prompts as keys. On API error, we return a fallback template with is_fallback: true flag so the backend knows to alert users."

**Q: How do you handle PII in vendor data?**
A: "We never log vendor details, only risk assessment outputs. Our prompts never request personal information, and we strip any email/phone patterns from inputs before processing."

**Q: What's your rate limiting strategy?**
A: "Flask-Limiter enforces 30 requests per minute per IP. We use X-Forwarded-For header in production to respect proxy headers. Excess requests get 429 Too Many Requests response."

**Q: How scalable is this?**
A: "With Redis clustering and Groq API free tier supporting 100+ req/min, we can handle enterprise scale. The containerized design allows horizontal scaling via Kubernetes."

## Final Checklist Before Presentation
- [ ] All 3 endpoints tested and working
- [ ] SECURITY.md ready to reference
- [ ] Demo script visible on screen
- [ ] Screenshots backed up locally
- [ ] API key confirmed active
- [ ] Redis cache verified
- [ ] Rate limit test ready
- [ ] Injection demo payload saved
- [ ] Team briefed on timing
- [ ] Talking points memorized (not reading)

**YOU ARE READY FOR THE PANEL.**