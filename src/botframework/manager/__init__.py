__all__ = ["application_manager", "register"]

from .application_manager import ApplicationManager

from .decorators import register  # noqa

application_manager = ApplicationManager()
