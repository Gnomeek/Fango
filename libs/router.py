from typing import Callable, Type

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from libs.viewset import ModelViewSet
    from flask import Blueprint


def register_api(app: Blueprint, view: Type[ModelViewSet], endpoint: str, url: str, pk='_id', pk_type='int'):
    view_func: Callable = view.as_view(endpoint)
    pk_rule_list = []
    for method in view.__methods__:
        method = method.upper()
        if method == "GET":
            app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])
        elif method == "POST":
            app.add_url_rule(url, view_func=view_func, methods=['POST'])
        else:
            pk_rule_list.append(method)
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=pk_rule_list)
