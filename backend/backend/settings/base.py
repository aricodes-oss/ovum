from pathlib import Path

from configurations import Configuration
from configurations.values import DatabaseURLValue


class Base(Configuration):
    """Shared settings for all environments."""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    SECRET_KEY = "django-insecure-^l0fmt8tuah=3=hy&oz!7-2i@n(t#f!$j5p9wgia8uhns6o9(^"

    ALLOWED_HOSTS = ["*"]

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "drf_spectacular",
        "backend",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "backend.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "backend.wsgi.application"

    DATABASES = DatabaseURLValue("postgres://postgres:postgres@database/postgres")

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "UTC"
    USE_I18N = True
    USE_TZ = True

    STATIC_URL = "static/"
    STATIC_ROOT = str(BASE_DIR / "staticfiles")

    REST_FRAMEWORK = {
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }

    SPECTACULAR_SETTINGS = {
        "TITLE": "Ovum API",
        "VERSION": "0.1.0",
    }
