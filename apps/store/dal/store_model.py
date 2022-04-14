from sqlalchemy import DECIMAL, Column, Integer, Text

from utils.db.model import Model
from utils.db.orm_model_base import CommonFieldsMixin


class StoreStorage(CommonFieldsMixin, Model):
    """
    CREATE TABLE store_storage (
        `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        `name` TEXT DEFAULT NULL,
        `price` decimal(10, 4) NOT NULL,
        `volume` int(11) DEFAULT 0,
        `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
    """

    __tablename__ = "store_storage"
    name = Column(Text, default="", comment="item name")
    price = Column(DECIMAL(10, 4), comment="item price")
    volume = Column(Integer, comment="item counts")

    @classmethod
    def create_data(cls, **kwargs):
        return cls.create(**kwargs)
