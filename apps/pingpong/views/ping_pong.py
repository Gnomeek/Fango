from flask import make_response, jsonify

from libs.viewset import ModelViewSet


class PingPong(ModelViewSet):
    __methods__ = ["GET"]

    def get_queryset(self):
        pass

    def get(self, _id):
        return make_response(jsonify({"msg": "pong"}), 200)
