import unittest
from milsymbserver import app

from flask.ext.testing import TestCase

class MilSymbTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app





class TestSidc(MilSymbTestCase):
    def test_invalid_sic_length(self):
        response = self.client.get('/sidc/123456/')
        self.assert404(response)

    def test_valid_sic(self):
        response = self.client.get('/sidc/10031002181211020000/')

if __name__ == '__main__':
    unittest.main()