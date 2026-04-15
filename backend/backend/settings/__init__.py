from backend.settings.base import Base
from backend.settings.local import Local

__all__ = ["Base", "Local"]


# Production is lazy-imported to avoid eagerly evaluating SecretValue
# fields (e.g. DJANGO_SECRET_KEY) when the module is loaded in non-production
# environments.
def __getattr__(name: str) -> type:
    if name == "Production":
        from backend.settings.production import Production

        return Production
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
