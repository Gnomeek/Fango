# coding: utf-8
import os

from configs import settings


LOG_DIR = os.path.join(settings.BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)  # 创建路径

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s %(levelname)s [%(filename)s][%(funcName)s][%(lineno)d] > %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file_handler_info": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "info.log"),
            "formatter": "default",
            "encoding": "utf-8",
            "when": "D",
            "interval": 1,
            "backupCount": 7,
        },
        "file_handler_error": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "formatter": "default",
            "encoding": "utf-8",
            "when": "D",
            "interval": 1,
            "backupCount": 7,
        },
        "request_handler": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "request.log"),
            "formatter": "default",
            "encoding": "utf-8",
            "when": "D",
            "interval": 1,
            "backupCount": 7,
        },
    },
    "root": {"handlers": ["console", "file_handler_info", "file_handler_error"], "level": "INFO"},
    "loggers": {
        "request": {
            "handlers": ["request_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
