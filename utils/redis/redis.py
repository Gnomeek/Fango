import redis

from configs import ENV_PROFILE, settings


def init_redis_client():
    if ENV_PROFILE in ["prod"]:
        client = None  # TODO
    else:
        client = redis.StrictRedis(host="localhost", port=6379, db=0)
    return client


if not settings.NO_REDIS:
    pass
else:
    redis_client = init_redis_client()
