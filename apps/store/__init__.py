from flask import Blueprint

from apps.store.views.store import StoreView
from libs.router import register_api


bp = Blueprint("store", __name__)

# 注册MethodView API到蓝图
register_api(app=bp, view=StoreView, endpoint="store", url="/items")
