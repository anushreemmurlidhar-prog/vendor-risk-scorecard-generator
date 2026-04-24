# Tool-93 Vendor Risk Scorecard Generator

A capstone project scaffold for Tool-93 with a Spring Boot backend, Flask AI microservice, and React + Vite frontend.

## Tech stack

- Java 17, Spring Boot 3.x
- Python 3.11, Flask 3.x
- PostgreSQL 15
- Redis 7
- React 18 + Vite
- Tailwind CSS
- Docker + Docker Compose
- Groq API for AI generation

## Setup

1. Copy `.env.example` to `.env` and add your `GROQ_API_KEY`.
2. Build and run all services:

```bash
docker-compose up --build
```

3. Access the services:

- Frontend: http://localhost
- Backend Swagger: http://localhost:8080/swagger-ui.html
- AI health: http://localhost:5000/health

## Project structure

- `backend/` — Spring Boot project and Flyway migrations
- `ai-service/` — Flask microservice for Groq AI calls
- `frontend/` — React + Vite UI
- `docker-compose.yml` — orchestrates all services

## Notes

- The backend is configured with environment placeholders in `backend/src/main/resources/application.yml`.
- The AI service includes prompt sanitization and rate limiting.
- The frontend is a basic React scaffold that checks backend health.
