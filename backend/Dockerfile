FROM python:3.14-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip install poetry

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root


FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/code/.venv/bin:$PATH" \
    DJANGO_CONFIGURATION=Production

RUN groupadd --system --gid 1000 app \
    && useradd --system --uid 1000 --gid app --create-home --home-dir /home/app app

WORKDIR /code

COPY --from=builder --chown=app:app /code/.venv /code/.venv
COPY --chown=app:app . .

USER app

CMD python manage.py wait_for_db && \
    python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    python manage.py createcachetable && \
    gunicorn -b 0.0.0.0:3000 backend.wsgi:application
