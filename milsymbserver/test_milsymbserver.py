import unittest
from jmsml import Sidc, InvalidSidcLength, MilSymbol
from milsymbserver import app

from flask.ext.testing import TestCase

class MilSymbTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app


class TestSidcClass(MilSymbTestCase):
    def test_sidc_length(self):
        self.assertRaises(InvalidSidcLength, Sidc, "123453")

    def test_version(self):
        sidc = Sidc("10031002181211020000")
        self.assertEquals("10", sidc.version)

    def test_context(self):
        sidc = Sidc("10031002181211020000")
        self.assertEquals("0", sidc.context)

    def test_standard_identity(self):
        sidc = Sidc("10031002181211020000")
        self.assertEquals("3", sidc.standard_identity)

    def test_concat(self):
        input_sidc = "12345678901234567890"
        sidc = Sidc(input_sidc)
        self.assertEquals(input_sidc, str(sidc))


class TestMilSymbol(MilSymbTestCase):
    def test_innit(self):
        symb = MilSymbol("10031002181211020000")
        self.assertEqual("sdfsd23423423f.svg", symb.frame_fn)



class TestSidc(MilSymbTestCase):
    def test_invalid_sic_length(self):
        response = self.client.get('/sidc/123456/')
        self.assert404(response)

    def test_valid_sic(self):
        response = self.client.get('/sidc/10031002181211020000/')


class TestResponseType(MilSymbTestCase):
    def test_svg_response(self):
        response = self.client.get('/sidc/10031002181211020000/')
        self.assertEqual("image/svg+xml", response.mimetype,)

    def test_testsymbol(self):
        response = self.client.get('/testsymbol')
        self.assertEqual("image/svg+xml", response.mimetype,)


if __name__ == '__main__':
    unittest.main()