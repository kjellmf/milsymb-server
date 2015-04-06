from pprint import pprint
from flask import abort
import flask
from milsymbserver import app

@app.route('/')
def index():
    return 'Hello World!'


def parse_sidc(sidc):
    if len(sidc) != 20:
        return
    d = {}
    d['version'] = sidc[0:2]
    d['context'] = sidc[2:3]
    d['standard_identity'] = sidc[3:4]
    d['symbolset'] = sidc[4:6]
    d['status'] = sidc[6:7]
    d['hqtfd'] = sidc[7:8]
    d['amplifier'] = sidc[8:9]
    d['amplifier_descriptor'] = sidc[9:10]
    d['entity'] = sidc[10:12]
    d['entity_type'] = sidc[12:14]
    d['entity_subtype'] = sidc[14:16]
    d['modifier_one'] = sidc[16:18]
    d['modifier_two'] = sidc[18:20]

    return d



@app.route('/sidc/<sic>/')
def sic(sic):
    if len(sic) != 20:
        app.logger.error('Invalid SIDC length')
        abort(404)
    elements = parse_sidc(sic)
    return flask.jsonify(elements)