import logging
import time
import traceback

from http import HTTPStatus
from typing import TYPE_CHECKING, Optional

from flask import g, jsonify, make_response, request

from utils.redis.redis import redis_client


if TYPE_CHECKING:
    from flask import Response

logger = logging.getLogger(__name__)


def authorization() -> Optional["Response"]:
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        app_id = redis_client.get("token-%s" % token)
        if app_id:
            app_id = app_id.decode("utf-8")
            g.app_id = app_id
            return None
        return make_response(jsonify({"msg": "invalid access token!", "code": -1}), HTTPStatus.FORBIDDEN)
    except Exception as e:
        logger.error(e)
        s = traceback.format_exc()
        logger.error(s)
        return make_response(jsonify({"msg": "server error!", "code": -1}), HTTPStatus.SERVICE_UNAVAILABLE)


def before_request_func():
    request.start_time = time.time()
    # add your middleware here


def after_request_logging(response) -> "Response":
    try:
        logger.info(
            "PATH: {0.path}, METHOD: {0.method}, response code: {1.status_code}, run_time: {2}".format(
                request, response, time.time() - request.start_time
            )
        )
    except Exception as e:
        logger.warning(e)
        pass
    return response


def after_request_func(response) -> "Response":
    after_request_logging(response)
    # add your middleware here
    return response
