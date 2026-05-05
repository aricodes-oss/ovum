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
        "django_dramatiq",
        "rest_framework",
        "drf_spectacular",
        "allauth",
        "allauth.account",
        "allauth.headless",
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
        "allauth.account.middleware.AccountMiddleware",
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

    VALKEY_URL = "redis://cache:6379"

    @property
    def CACHES(self) -> dict:
        return {
            "default": {
                "BACKEND": "django_valkey.cache.ValkeyCache",
                "LOCATION": f"{self.VALKEY_URL}/1",
            }
        }

    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

    @property
    def DRAMATIQ_BROKER(self) -> dict:
        return {
            "BROKER": "dramatiq.brokers.redis.RedisBroker",
            "OPTIONS": {
                "url": f"{self.VALKEY_URL}/0",
            },
            "MIDDLEWARE": [
                "dramatiq.middleware.AgeLimit",
                "dramatiq.middleware.TimeLimit",
                "dramatiq.middleware.Callbacks",
                "dramatiq.middleware.Retries",
                "django_dramatiq.middleware.DbConnectionsMiddleware",
                "django_dramatiq.middleware.AdminMiddleware",
            ],
        }

    @property
    def DRAMATIQ_RESULT_BACKEND(self) -> dict:
        return {
            "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
            "BACKEND_OPTIONS": {
                "url": f"{self.VALKEY_URL}/2",
            },
            "MIDDLEWARE_OPTIONS": {
                "result_ttl": 1000 * 60 * 10,
            },
        }

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

    STATIC_URL = "api/static/"
    STATIC_ROOT = str(BASE_DIR / "staticfiles")

    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    ]

    #
    # Allauth
    #
    HEADLESS_ONLY = True
    ACCOUNT_EMAIL_VERIFICATION = "none"
    # Note: allauth.socialaccount is intentionally excluded from INSTALLED_APPS
    # to disable social account login.

    REST_FRAMEWORK = {
        "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    }

    CSRF_TRUSTED_ORIGINS = ["http://*", "http://*"]

    SPECTACULAR_SETTINGS = {
        "TITLE": "Ovum API",
        "VERSION": "0.1.0",
        "POSTPROCESSING_HOOKS": [
            "drf_standardized_errors.openapi_hooks.postprocess_schema_enums",
            "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
        ],
        "SERVE_INCLUDE_SCHEMA": False,
        "COMPONENT_SPLIT_REQUEST": True,
        "CAMELIZE_NAMES": False,  # Perform this with POSTPROCESSING_HOOKS instead
        "ENUM_NAME_OVERRIDES": {
            "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices",
            "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices",
            "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices",
            "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices",
            "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices",
            "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices",
            "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices",
            "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices",
            "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices",
            "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices",
            "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices",
        },
    }
