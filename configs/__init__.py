import importlib
import os


ENV_PROFILE = os.getenv("FLASK_ENV", "dev")
settings = importlib.import_module("configs.%s" % ENV_PROFILE)
