from importlib import import_module


def import_attr(path):
    modules = path.split(".")
    module_name = ".".join(modules[:-1])
    attr_name = modules[-1]
    return getattr(import_module(module_name), attr_name)
