# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ovum is a full-stack web application with a Django REST API backend and Next.js frontend, orchestrated via Docker Compose behind a Caddy reverse proxy.

## Architecture

- **frontend/** — Next.js 16 (App Router) with React 19, TypeScript, React Compiler enabled
- **backend/** — Django 6 with Django REST Framework, PostgreSQL, Valkey cache
- **Caddy** reverse proxy on port 3000: routes `/api/*` to backend, everything else to frontend
- Both services run on port 3000 internally; Caddy is the external entry point

## Development

Start all services (frontend, backend, PostgreSQL, Valkey, Caddy):
```
docker compose up
```
Both frontend and backend have volume mounts for live reload during development.

**Always prefer `docker compose exec` for running commands against services. Use `docker compose run --rm` only for one-off commands where the service is not already running.** Do not `cd` into a project directory and run commands on the host directly.

### Frontend (frontend/)
```bash
docker compose exec frontend npm run dev       # Next.js dev server
docker compose exec frontend npm run build     # Production build
docker compose exec frontend npm run lint      # ESLint
docker compose exec frontend npm install <package>  # Add a dependency
```
- TypeScript path alias: `@/*` maps to project root
- ESLint 9 with next/core-web-vitals and next/typescript configs

### Backend (backend/)
```bash
docker compose exec backend poetry run python manage.py runserver 0.0.0.0:3000   # Dev server
docker compose exec backend poetry run python manage.py migrate                    # Run migrations
docker compose exec backend poetry run python manage.py createsuperuser            # Create admin user
docker compose exec backend poetry add <package>                               # Add a dependency
```
- Poetry for dependency management
- Configuration via environment variables (django-environ): `DATABASE_URL`, `DJANGO_PRODUCTION`, `DJANGO_DEBUG`
- Default DB connection: `postgres://postgres:postgres@database/postgres`
- Admin panel at `/admin/`

## Important: Next.js 16 Breaking Changes

Next.js 16 has breaking changes from what may be in training data. **Always read the relevant guide in `frontend/node_modules/next/dist/docs/` before writing Next.js code.** Heed deprecation notices.
