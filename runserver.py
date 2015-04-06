# -*- coding: utf-8 -*-
import logging
import os

from milsymbserver import app

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    print os.path.abspath(app.config["SVG_PATH"])
    app.run(debug=True)