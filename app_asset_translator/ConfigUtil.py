import yaml


def get_config():
    return yaml.safe_load(open("app-asset-translator.yaml"))
