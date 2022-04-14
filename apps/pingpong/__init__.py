from flask import Blueprint

from apps.pingpong.views.ping_pong import PingPong
from libs.router import register_api


bp = Blueprint("pingpong", __name__)

# 注册MethodView API到蓝图
register_api(app=bp, view=PingPong, endpoint="ping_pong", url="/ping")
