# Ovum

Ovum is a template for a full-stack web application with a Django REST API backend and Next.js frontend, orchestrated via Docker Compose behind a Caddy reverse proxy.

## Architecture

- **Frontend**: Next.js 16 (App Router)
- **Backend**: Django 6 with Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Valkey
- **Proxy**: Caddy (external port 3000)

## Quick Start

Ensure you have Docker and Docker Compose installed.

1.  **Clone the repository**
2.  **Start all services**
    ```bash
    docker compose up
    ```
3.  **Access the application**
    - Frontend: [http://localhost:3000](http://localhost:3000)

## Development Commands

### Frontend
```bash
docker compose exec frontend npm run dev       # Next.js dev server
docker compose exec frontend npm run lint      # ESLint
docker compose exec frontend npm install <pkg> # Add package
```

### Backend
```bash
docker compose exec backend poetry run python manage.py migrate      # Run migrations
docker compose exec backend poetry run python manage.py createsuperuser # Create admin
docker compose exec backend poetry add <pkg>                         # Add dependency
```

## Testing

```bash
docker compose exec backend poetry run pytest        # Backend tests
docker compose exec backend poetry run ruff check .  # Backend lint
docker compose exec backend poetry run mypy .        # Backend types
docker compose exec frontend npm run lint            # Frontend lint
docker compose exec frontend npm run typecheck       # Frontend types
docker compose exec frontend npm test -- --run       # Frontend unit tests (Vitest)
docker compose exec frontend npm run test:e2e        # Frontend E2E (Playwright)
```

CI runs all of the above on push (`.github/workflows/ci.yml`). A
`.pre-commit-config.yaml` is included — install with `pip install pre-commit && pre-commit install`.

## Production Checklist

Local development uses safe defaults from `backend/backend/settings/local.py`
and does **not** require any environment variables. For production:

1. Set `DJANGO_CONFIGURATION=Production`.
2. Provide every variable from `backend/.env.example`. `django-configurations`
   will fail to start if any required value is missing.
3. Generate a fresh `DJANGO_SECRET_KEY` (e.g. `python -c 'import secrets; print(secrets.token_urlsafe(64))'`).
4. Narrow `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` to your
   actual hostnames — do **not** copy the wildcards from `local.py`.
5. Front the stack with TLS (Caddy auto-provisions certs when the site
   address in `Caddyfile` is a real hostname rather than `:3000`).

## Project Structure

- `frontend/`: Next.js application
- `backend/`: Django REST API
- `Caddyfile`: Reverse proxy configuration
- `docker-compose.yml`: Service orchestration
- `.github/workflows/ci.yml`: Lint, type-check, test, build
