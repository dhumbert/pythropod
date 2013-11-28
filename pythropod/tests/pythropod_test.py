import unittest
import grequests
from pythropod.pythropod import Pythropod

# todo verify that test passed/failed
class PythropodTestCase(unittest.TestCase):
    def test_pythropod(self):
        test = {'id': 666, 'url': 'http://dhwebco.com', 'type': 'text', 'text': 'Lorem'}
        p = Pythropod(test, None, grequests.Pool(), request=_dummyRequest)
        p.run()


def _dummyRequest(url, callback, pool):
    callback("""
        <html>
            <body>
                Lorem ipsum dolor sit amet.
            </body>
        </html>
        """)


if __name__ == '__main__':
    unittest.main()
