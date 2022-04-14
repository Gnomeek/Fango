from sqlalchemy import create_engine

from configs import settings
from libs.tools import import_attr


class Engine(object):
    def __init__(self, config):
        self.config = config

    def get_engine(self, db_name=None):
        raise NotImplementedError()


class MysqlEngine(Engine):
    engine = None

    def get_engine(self, db_name=None):
        db_url = "mysql+pymysql://%s:%s@%s:%s/%s?charset=%s" % (
            self.config.get("USER", ""),
            self.config.get("PASSWORD", ""),
            self.config.get("HOST", ""),
            self.config.get("PORT", "3306"),
            self.config.get("DB_NAMES", {}).get(db_name) if db_name else self.config.get("NAME", ""),
            self.config.get("CHARSET", "utf8mb4"),
        )
        if self.engine is None:
            self.engine = create_engine(db_url, pool_recycle=60 * 5)
        return self.engine


read_engine_instance = None
write_engine_instance = None


def get_engine(readonly=True, db_name=None):
    db_config = settings.DATABASES.get("read" if readonly else "write") or settings.DATABASES.get("default")
    engine_cls = import_attr(db_config.get("ENGINE"))
    global read_engine_instance
    global write_engine_instance
    if readonly:
        if read_engine_instance is None:
            read_engine_instance = engine_cls(db_config)
        return read_engine_instance.get_engine()
    else:
        if write_engine_instance is None:
            write_engine_instance = engine_cls(db_config)
        return write_engine_instance.get_engine()
