from configparser import ConfigParser
from os import path


def get_config():
    config = ConfigParser()
    config.read(path.join(path.dirname(__file__), 'config.ini'))
    return config['DEFAULT']
