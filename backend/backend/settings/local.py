from backend.settings.base import Base


class Local(Base):
    """Local development configuration."""

    DEBUG = True

    SECRET_KEY = "django-insecure-^l0fmt8tuah=3=hy&oz!7-2i@n(t#f!$j5p9wgia8uhns6o9(^"
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = ["https://*", "http://*"]
