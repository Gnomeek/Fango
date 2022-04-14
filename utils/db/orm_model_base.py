# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer


class CommonFieldsMixin(object):
    """
    basic ORM keys mixin
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime(), default=datetime.now)
