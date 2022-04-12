import flask
from apps.pingpong import bp as demo_app
from configs import ENV_PROFILE
# from libs.hooks import after_request_func, before_request_func
# from logging_config import config as logging_config
# import logging
#
# # 初始化log
# logging.config.dictConfig(logging_config)
# logger = logging.getLogger(__name__)

# 初始化server
server = flask.Flask(__name__)

# 注册蓝图
server.register_blueprint(demo_app, url_prefix='/api/pingpong')

# 注册请求钩子
# server.before_request(before_request_func)
# server.after_request(after_request_func)

# 调试模式
if ENV_PROFILE == 'dev':
    server.debug = True
    server.run()

if __name__ == '__main__':
    server.run()
