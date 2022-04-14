import logging

from http import HTTPStatus
from typing import Dict

from flask import jsonify, make_response, request

from apps.store.dal.store_model import StoreStorage
from libs.viewset import ModelViewSet


logger = logging.getLogger(__name__)


class StoreView(ModelViewSet):

    __methods__ = ["GET", "POST"]
    OBJ_MODEL = StoreStorage

    def get_queryset(self):
        param: Dict = request.args
        _id = param.get("_id")
        logger.info(f"request searches for record that id = {param}")
        return self.OBJ_MODEL.filter(self.OBJ_MODEL.id == _id)

    def post(self):
        try:
            request_data: Dict = request.json
            logger.info(f"request write record = {request_data}")
            created_data = self.OBJ_MODEL.create_data(**request_data)
            return make_response(jsonify(created_data.to_dict()), HTTPStatus.OK)
        except Exception as e:
            logger.error(f"create data failed with error: {e}")
            return make_response(jsonify({"msg": "internal error!", "code": -1}), HTTPStatus.INTERNAL_SERVER_ERROR)
