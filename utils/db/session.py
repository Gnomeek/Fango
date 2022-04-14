#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
provide session
"""
from contextlib import contextmanager
from functools import wraps

from sqlalchemy.orm import scoped_session, session as ss, sessionmaker

from utils.db.engines import get_engine


def _session(readonly=False, db=None) -> ss:
    """
    create a session
    """
    engine = get_engine(readonly=readonly, db_name=db)
    # todo: add args like pool size.
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))
    return session


@contextmanager
def create_session(readonly=False, db=None):
    """
    create a session, and close it after query

    with create_session() as session:
        session.query(User).all()

    no need to close it manually
    """
    session = _session(readonly, db)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# distinguish read and write session
def provide_session(readonly=False, db=None):
    """
    provide session to a function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            arg_session = "session"

            session_in_kwargs = arg_session in kwargs

            if session_in_kwargs:
                return func(*args, **kwargs)
            else:
                with create_session(readonly, db) as session:
                    kwargs[arg_session] = session
                    return func(*args, **kwargs)

        return wrapper

    return decorator


def write_session():
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=get_engine(readonly=False), expire_on_commit=False)
    )
    return session()
