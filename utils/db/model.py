from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import Query

from utils.db.session import provide_session, write_session


class BaseDao:
    def obj2dict(self, obj):
        result = []
        # get available columns of an object
        for item in obj:
            res = {}
            cols = item.__table__.columns
            for col in cols:
                res[col.name] = getattr(item, col.name)
            result.append(res)
        return result


class BaseQuery(Query):
    def update(self, values, synchronize_session="evaluate", update_args=None):
        self.session = write_session()
        result = super().update(values, synchronize_session, update_args)
        self.session.commit()
        return result

    def delete(self, synchronize_session="evaluate"):
        self.session = write_session()
        result = super().delete(synchronize_session)
        self.session.commit()
        return result


class Model(declarative_base()):
    """
    SQLAlchemy ORM Model的基类，实现所有Model的共通方法，以及类似 django ORM 的用法.
    例: 有一个继承基类的Model: class Project(Model): ...
    增加: Project.create(project_id=1, name="xxx")
    查询: Project.filter(project_id=1, name="xxx")
    更新: Project.filter(project_id=1, name="xxx").update({"name": "123"})
    删除: Project.filter(project_id=1, name="xxx").delete()

    """

    __abstract__ = True

    def to_dict(self) -> dict:
        """
        model对象转化为字典
        :return:
        """

        return {k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"}

    @classmethod
    def get_column_params(cls, origin_dict: dict) -> dict:
        """
        从字典中获取所有key为column的pair，组成新字典
        :param origin_dict:
        :return:
        """
        params = dict()
        for (key, value) in origin_dict.items():
            if key in cls.__table__.columns:
                params[key] = value
        return params

    @classmethod
    @provide_session(readonly=True)
    def filter(cls, *args, **kwargs) -> Query:
        """
        通用的filter方法，后面可直接接update(),delete()方法
        :param kwargs: 过滤条件
        :return: BaseQuery
        """
        session = kwargs["session"]
        params = cls.get_column_params(kwargs)
        query = session.query(cls).filter(*args).filter_by(**params)
        query.__class__ = BaseQuery
        return query

    @classmethod
    @provide_session(readonly=False)
    def create(cls, **kwargs):
        """
        通用的create方法
        :param kwargs:
        :return:
        """
        session = kwargs["session"]
        params = cls.get_column_params(kwargs)
        obj = cls(**params)
        session.add(obj)
        return obj

    @classmethod
    @provide_session(readonly=False)
    def bulk_create(cls, objects, **kwargs):
        """
        通用的bulk_create方法
        :param kwargs:
        :return:
        """
        session = kwargs["session"]
        session.bulk_save_objects(objects)
