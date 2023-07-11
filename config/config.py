"""
This module provides a configuration reader for accessing values from the config.ini file.
"""

from configparser import RawConfigParser

config = RawConfigParser()
config.read("config/config.ini")

API_KEY = config.get("API", "API_KEY")
BASE_URL = config.get("API", "BASE_URL")
TIME_OUT = config.getint("API", "TIME_OUT")
