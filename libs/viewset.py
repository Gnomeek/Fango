import logging

from http import HTTPStatus

from flask import jsonify, make_response, request
from flask.views import MethodView


logger = logging.getLogger(__name__)


class ModelViewSet(MethodView):
    __methods__ = ["GET", "POST", "PUT"]

    def get_queryset(self):
        raise NotImplementedError

    @staticmethod
    def paginate_queryset(queryset):
        params = request.args
        page = int(params.get("page", 1))
        page_size = int(params.get("page_size", 10))
        return queryset.limit(page_size).offset((page - 1) * page_size)

    def get(self, _id):
        try:
            queryset = self.get_queryset()
            paged_qs = self.paginate_queryset(queryset)
            data = [{k: v for k, v in obj.to_dict().items()} for obj in paged_qs]
            return make_response(jsonify({"count": queryset.count(), "data": data, "code": 200}), HTTPStatus.OK)
        except Exception as e:
            logger.error(f"get data failed with error: {e}")
            return make_response(jsonify({"msg": "internal error!", "code": -1}), HTTPStatus.INTERNAL_SERVER_ERROR)
