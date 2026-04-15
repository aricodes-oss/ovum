from configurations.values import SecretValue

from backend.settings.base import Base


class Production(Base):
    """Production configuration."""

    DEBUG = False

    SECRET_KEY = SecretValue(environ_name="DJANGO_SECRET_KEY")
