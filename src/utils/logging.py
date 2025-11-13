"""
Loguru logging configuration for Django.
"""

import sys
import logging
import os

from loguru import logger

DEFAULT_PREFIX = "Django"


class InterceptHandler(logging.Handler):
    """
    Intercept standard logging messages and redirect to loguru
    """

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure(
    prefix: str = None, intercept_django: bool = True, intercept_gunicorn: bool = True
):
    """
    Configure loguru logging.

    Args:
        prefix: Log prefix (defaults to LOG_PREFIX env var or DEFAULT_PREFIX)
        intercept_django: Intercept Django's logging
        intercept_gunicorn: Intercept Gunicorn's logging
    """
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    prefix = prefix or os.environ.get("LOG_PREFIX", DEFAULT_PREFIX)

    log_format = (
        f"{prefix} "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> - <level>{message}</level>"
    )

    logger.remove()
    logger.add(sys.stdout, colorize=True, level=log_level, format=log_format)

    if intercept_django:
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        for logger_name in ["django", "django.request", "django.db.backends"]:
            django_logger = logging.getLogger(logger_name)
            django_logger.handlers = [InterceptHandler()]
            django_logger.propagate = False

    if intercept_gunicorn:
        for logger_name in ["gunicorn", "gunicorn.access", "gunicorn.error"]:
            gunicorn_logger = logging.getLogger(logger_name)
            gunicorn_logger.handlers = [InterceptHandler()]
            gunicorn_logger.propagate = False
