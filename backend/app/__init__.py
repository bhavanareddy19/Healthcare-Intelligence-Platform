"""
Healthcare Intelligence Platform - Backend App Package
"""

# Lazy import to avoid circular imports
def get_settings():
    from .config import get_settings as _get_settings
    return _get_settings()

__all__ = ["get_settings"]
