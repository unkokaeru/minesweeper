"""logging.py: Logging Configuration File"""

from rich.logging import RichHandler

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(message)s",
    "datefmt": "[%X]",
    "handlers": [RichHandler(rich_tracebacks=True)],
}
