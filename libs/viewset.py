from flask import make_response, jsonify, request
from flask.views import MethodView


class ModelViewSet(MethodView):
    DICT_DEPTH = 1
    __methods__ = ["GET", "POST", "PUT"]

    # @abc.abstractmethod
    def get_queryset(self):
        """

        :return:
        :rtype:
        """
        raise NotImplementedError

    @staticmethod
    def paginate_queryset(queryset):
        params = request.args
        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 10))
        return queryset.limit(page_size).offset((page - 1) * page_size)

    def get(self, _id):
        queryset = self.get_queryset()
        paged_qs = self.paginate_queryset(queryset)
        data = []
        for obj in paged_qs:
            d = {k: v for k, v in obj.to_dict(depth=self.DICT_DEPTH).items()}
            data.append(d)
        return make_response(jsonify({'count': queryset.count(), 'data': data, 'code': 200}), 200)
