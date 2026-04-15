"""Custom mypy plugin that installs the django-configurations importer
before django-stubs initializes Django settings.

Workaround for https://github.com/typeddjango/django-stubs/issues/1709
From https://github.com/typeddjango/django-stubs/pull/180#issuecomment-820062352
"""

import os

from configurations.importer import install
from mypy_django_plugin import main


def plugin(version: str) -> type:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
    install()
    return main.plugin(version)
