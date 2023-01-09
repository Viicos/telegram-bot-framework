import logging

from typing_extensions import Literal

LogLevels = Literal["debug", "info", "warning", "error", "critical"]

name_to_level = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
