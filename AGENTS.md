# Ovum Agent Guide

## Architecture & Routing
- **Full Stack**: Django 6 (Backend) + Next.js 16 (Frontend) + Caddy (Proxy) + PostgreSQL + Valkey.
- **Entrypoint**: Caddy on port 3000.
  - `/api/*` -> Backend (Django)
  - `/*` -> Frontend (Next.js)
- **Service Ports**: Both frontend and backend run on port 3000 internally within the Docker network.

## Critical Workflow: "Always use Docker"
Do NOT run commands on your host. Always use `docker compose exec`.

### Backend (Django)
- **Configuration**: Uses `django-configurations`. 
  - `DJANGO_CONFIGURATION=Local` (default) or `Production`.
  - Settings are classes in `backend/backend/settings/`.
- **Commands**:
  - `docker compose exec backend poetry run python manage.py <command>`
  - `docker compose exec backend poetry run pytest` (Tests)
  - `docker compose exec backend poetry run ruff check .` (Lint)
  - `docker compose exec backend poetry run mypy .` (Type check)
- **Mypy Note**: Uses a custom plugin `backend/configurations_mypy_plugin.py` to handle `django-configurations`.

### Frontend (Next.js)
- **Versions**: Next.js 16 (App Router), React 19, React Compiler enabled.
- **API Client**: Generated via **Orval**. 
  - **Command**: `docker compose exec frontend npm run api:generate`
  - This reads the schema from the backend (must be running).
  - Target files: `frontend/api/backend.ts` and `frontend/api/allauth.ts`.
  - **Custom Mutator**: Uses `frontend/api/mutator/custom-instance.ts` for Axios. Check this for base URL or header logic.
- **Commands**:
  - `docker compose exec frontend npm run dev`
  - `docker compose exec frontend npm run lint`

## Verification Order
When submitting changes:
1. **Backend**: `ruff` -> `mypy` -> `pytest`
2. **Frontend**: `lint` -> `build` (if significant changes)
3. **Integration**: If API changes, run `api:generate` and check frontend for breakages.

## Gotchas
- **Valkey**: We use `valkey` image, not `redis`.
- **Next.js 16**: APIs and conventions differ from training data. Refer to `node_modules/next/dist/docs/` in the frontend container if unsure.
- **Headless Auth**: `django-allauth` is in headless mode. All auth is handled via API.
