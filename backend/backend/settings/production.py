from configurations.values import DatabaseURLValue, ListValue, SecretValue, Value

from backend.settings.base import Base


class Production(Base):
    """Production configuration."""

    DEBUG = False

    SECRET_KEY = SecretValue(environ_name="DJANGO_SECRET_KEY")

    DATABASES = DatabaseURLValue(environ_required=True)
    VALKEY_URL = Value(environ_required=True)
    ALLOWED_HOSTS = ListValue(environ_required=True)
    CSRF_TRUSTED_ORIGINS = ListValue(environ_required=True)
