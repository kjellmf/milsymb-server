# -*- coding: utf-8 -*-
"""Code for retrieving data from the JMSML project"""
import json
from os.path import normpath, join, exists
from milsymbserver import app

_JMSML = {}


def _load_jmsml_data(json_filepath):
    global _JMSML
    with open(json_filepath) as f:
        _JMSML = json.load(f)

    print _JMSML["affiliations"]


# Note: For full-frame main icons (main icons that touch the frame), there is an additional suffix depending on the frame that the icon must touch:
# _0 = Unknown
# _1 = Friend
# _2 = Neutral
# _3 = Hostile
_SID_FILE_SUFFIX_MAPPING = {
    "0": "0",
    "1": "0",
    "2": "1",
    "3": "1",
    "4": "2",
    "5": "3",
    "6": "3",

}


class SymbolMappings(object):
    def __init__(self, jmsml_data):
        self._data = jmsml_data
        self._create_standard_identity_mappings()
        self._create_context_mappings()
        self._create_symbolset_mappings()

    def _create_standard_identity_mappings(self):
        self._si_mappings = {}
        for si in self._data["standardIdentities"]:
            self._si_mappings[si["digits"]] = si["id"]

    def _create_context_mappings(self):
        self._context_mappings = {}
        for context in self._data["contexts"]:
            self._context_mappings[context["digits"]] = context["id"]

    @property
    def standard_identity(self):
        return self._si_mappings

    @property
    def context(self):
        return self._context_mappings

    def _create_symbolset_mappings(self):
        self._symbol_set_mappings = {}
        for symbol_set in self._data["symbolSets"]:
            self._symbol_set_mappings[symbol_set["digits"]] = symbol_set

    @property
    def symbol_sets(self):
        return self._symbol_set_mappings


_load_jmsml_data(app.config["DATA_FILE"])
_SVG_PATH = app.config["SVG_PATH"]

mappings = SymbolMappings(_JMSML)


class InvalidSidc(Exception):
    """The symbol identification code is invalid"""


class InvalidSidcLength(InvalidSidc):
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
                    self.amplifier, self.amplifier_descriptor, self.entity, self.entity_type, self.entity_subtype,
                    self.modifier_one, self.modifier_two]
        return "".join(segments)


class MilSymbol(object):
    """Representation of a MILSTD 2525D/APP6D symbol"""

    def __init__(self, sidc):

        self.sidc = Sidc(sidc)
        self._frame_fn = None
        self._main_icon_fn = None
        self._mod_one_fn = None
        self._mod_two_fn = None

        self._init_ids()
        self._find_frame_fn()
        self._find_main_icon_fn()

    @property
    def frame_fn(self):
        if not self._frame_fn:
            self._find_frame_fn()
        return self._frame_fn

    @property
    def main_icon_fn(self):
        if not self._main_icon_fn:
            self._find_main_icon_fn()
        return self._main_icon_fn

    @property
    def mod_one_fn(self):
        if not self._mod_one_fn:
            self._find_mod_one_fn()
        return self._mod_one_fn

    @property
    def mod_two_fn(self):
        if not self._mod_two_fn:
            self._find_mod_two_fn()
        return self._mod_two_fn

    def _find_frame_fn(self):
        affiliations = _JMSML["affiliations"]
        try:
            frame_data = affiliations[self._context_id][self._dimension_id][self._standard_identity_id]
        except KeyError:
            raise InvalidSidc
        if self.sidc.status == "1" and "plannedGraphic" in frame_data:
            frame_fn = frame_data["plannedGraphic"]
        else:
            frame_fn = frame_data["graphic"]
        self._frame_fn = normpath(join(_SVG_PATH, frame_fn))

    def _init_ids(self):
        self._context_id = mappings.context.get(self.sidc.context)
        self._standard_identity_id = mappings.standard_identity.get(self.sidc.standard_identity)
        self._symbol_set = mappings.symbol_sets.get(self.sidc.symbolset, {})
        self._symbol_set_path = self._symbol_set.get("graphicFolder", {}).get("entities")
        self._mod_one_path = self._symbol_set.get("graphicFolder", {}).get("modifierOnes")
        self._mod_two_path = self._symbol_set.get("graphicFolder", {}).get("modifierTwos")
        self._dimension_id = self._symbol_set.get("dimensionId")

    def _find_main_icon_fn(self):
        fn = self.sidc.symbolset + self.sidc.entity + self.sidc.entity_type + self.sidc.entity_subtype
        full_frame_fn = join(_SVG_PATH, self._symbol_set_path, fn + "_" \
                             + _SID_FILE_SUFFIX_MAPPING[self.sidc.standard_identity] + ".svg")
        if exists(full_frame_fn):
            self._main_icon_fn = full_frame_fn
        else:
            self._main_icon_fn = join(_SVG_PATH, self._symbol_set_path, fn + ".svg")

    def _find_mod_one_fn(self):
        if self.sidc.modifier_one != "00" and self._mod_one_path:
            fn = self.sidc.symbolset + self.sidc.modifier_one + "1"
            self._mod_one_fn = join(_SVG_PATH, self._mod_one_path, fn + ".svg")

    def _find_mod_two_fn(self):
        if self.sidc.modifier_two != "00" and self._mod_two_path:
            fn = self.sidc.symbolset + self.sidc.modifier_two + "2"
            self._mod_two_fn = join(_SVG_PATH, self._mod_two_path, fn + ".svg")

