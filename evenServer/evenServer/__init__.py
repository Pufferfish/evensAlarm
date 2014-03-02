# -*- coding: utf-8 -*-
from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
  DEBUG = True,
    DATABASE = os.path.join(app.root_path, 'alarms.db'),
    PASSWORD = "passord",
    USERNAME = "bruker",
    SECRET_KEY='development key'
))

app.config.from_envvar('ALARM_SETTINGS', silent=True)

import evenServer.handlersi
