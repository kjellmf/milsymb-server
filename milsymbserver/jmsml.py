# -*- coding: utf-8 -*-
"""Code for retrieving data from the JMSML project"""
import json
from milsymbserver import app

_JMSML = {}

def _load_jmsml_data(json_filepath):
    global _JMSML
    with open(json_filepath) as f:
        _JMSML = json.load(f)

_load_jmsml_data(app.config["DATA_FILE"])


class InvalidSidcLength(Exception):
    """The symbol identification code has an invalid length"""


class Sidc(object):
    """Representation of a 20-digit symbol identification code"""
    def __init__(self, sidc):
        if len(sidc) != 20:
            raise InvalidSidcLength
        self.version = sidc[0:2]
        self.context = sidc[2:3]
        self.standard_identity = sidc[3:4]
        self.symbolset = sidc[4:6]
        self.status = sidc[6:7]
        self.hqtfd = sidc[7:8]
        self.amplifier = sidc[8:9]
        self.amplifier_descriptor = sidc[9:10]
        self.entity = sidc[10:12]
        self.entity_type = sidc[12:14]
        self.entity_subtype = sidc[14:16]
        self.modifier_one = sidc[16:18]
        self.modifier_two = sidc[18:20]

    def __str__(self):
        segments = [self.version, self.context, self.standard_identity, self.symbolset, self.status, self.hqtfd,
                    self.amplifier, self.amplifier_descriptor, self.entity, self.entity_type, self.entity_subtype, self.modifier_one, self.modifier_two]
        return "".join(segments)


class MilSymbol(object):
    def __init__(self, sidc):
        self.sidc = Sidc(sidc)
        self._frame_fn = None

    @property
    def frame_fn(self):
        if not self._frame_fn:
            self._find_frame_fn()
        return self._frame_fn

    def _find_frame_fn(self):
        self._frame_fn = "TTTTT.SVG"




