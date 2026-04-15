from backend.settings.base import Base


class Local(Base):
    """Local development configuration."""

    DEBUG = True
