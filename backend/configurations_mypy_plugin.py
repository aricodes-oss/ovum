"""Custom mypy plugin that installs the django-configurations importer
before django-stubs initializes Django settings.

Workaround for https://github.com/typeddjango/django-stubs/issues/1709
From https://github.com/typeddjango/django-stubs/pull/180#issuecomment-820062352
"""

import os

from mypy_django_plugin import main

from configurations.importer import install


def plugin(version: str) -> type:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
    install()
    return main.plugin(version)
