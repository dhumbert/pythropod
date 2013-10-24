import unittest
from pythropod.pythropod import Pythropod

class PythropodTestCase(unittest.TestCase):
    def test_pythropod(self):
        test = {'url': 'http://dhwebco.com', 'type': 'text', 'text': 'Lorem'}
        p = Pythropod(test, request=_dummyRequest)
        p.run()


def _dummyRequest(url, callback):
    callback("""
        <html>
            <body>
                Lorem ipsum dolor sit amet.
            </body>
        </html>
        """)


if __name__ == '__main__':
    unittest.main()
