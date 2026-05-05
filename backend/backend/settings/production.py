from configurations.values import (
    BooleanValue,
    DatabaseURLValue,
    EmailURLValue,
    IntegerValue,
    ListValue,
    SecretValue,
    Value,
)

from backend.settings.base import Base


class Production(Base):
    """Production configuration."""

    DEBUG = False

    SECRET_KEY = SecretValue(environ_name="DJANGO_SECRET_KEY")

    DATABASES = DatabaseURLValue(environ_required=True)
    VALKEY_URL = Value(environ_required=True)
    ALLOWED_HOSTS = ListValue(environ_required=True)
    CSRF_TRUSTED_ORIGINS = ListValue(environ_required=True)

    # Security headers. Caddy terminates TLS in front of Django, so we trust
    # X-Forwarded-Proto to detect HTTPS for SECURE_SSL_REDIRECT and secure cookies.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = BooleanValue(True)
    SECURE_HSTS_SECONDS = IntegerValue(60 * 60 * 24 * 365)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = BooleanValue(True)
    SECURE_HSTS_PRELOAD = BooleanValue(True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Email — defaults to console backend if EMAIL_URL is unset, which will
    # surface in logs. Set EMAIL_URL (e.g. submission://user:pass@smtp.host:587)
    # to actually deliver mail. Allauth password reset / email verification
    # require this.
    EMAIL = EmailURLValue("console://")
    DEFAULT_FROM_EMAIL = Value("webmaster@localhost")
    SERVER_EMAIL = Value("root@localhost")

    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
