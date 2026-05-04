# Ovum

Ovum is a full-stack web application with a Django REST API backend and Next.js frontend, orchestrated via Docker Compose behind a Caddy reverse proxy.

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
    - Frontend/API: [http://localhost:3000](http://localhost:3000)
    - Django Admin: [http://localhost:3000/admin/](http://localhost:3000/admin/)

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

## Project Structure

- `frontend/`: Next.js application
- `backend/`: Django REST API
- `Caddyfile`: Reverse proxy configuration
- `docker-compose.yml`: Service orchestration
