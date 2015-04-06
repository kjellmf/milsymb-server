# -*- coding: utf-8 -*-
import os
from flask import Flask
app = Flask(__name__)

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
app.config['JMSML_PATH'] = os.path.join(PROJECT_PATH, "../../joint-military-symbology-xml")
app.config['SVG_PATH'] = os.path.abspath(os.path.join(app.config['JMSML_PATH'], 'svg/MIL_STD_2525D_Symbols'))

try:
    app.config.from_envvar('MILSYMBSERVER_SETTINGS')
except RuntimeError:
    app.logger.warning('Could not load config')
    pass


import milsymbserver.views

