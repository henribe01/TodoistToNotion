from configparser import ConfigParser
from os import path


def get_config():
    config = ConfigParser()
    config.read(path.join(path.dirname(__file__), 'config.ini'))
    return config


def write_config(config):
    with open(path.join(path.dirname(__file__), 'config.ini'), 'w') as configfile:
        config.write(configfile)
