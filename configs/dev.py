from .default import *


SERVER_TARGET = "tcp://0.0.0.0:1234"
# change your db info
DATABASES = {
    "default": {
        "ENGINE": "utils.db.engines.MysqlEngine",
        "NAME": os.environ.get("DB_NAME", ""),
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWD", ""),
        "HOST": "localhost",
        "PORT": "3306",
    },
}
