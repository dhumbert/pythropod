import unittest
from pythropod.matchers import TextMatcher


dummyHtml = """
        <html>
            <body>
                Lorem ipsum dolor sit amet.
            </body>
        </html>
        """

class MatcherTestCase(unittest.TestCase):
    def test_pythropod(self):
        m = TextMatcher({'text': 'lorem'})
        m.match(dummyHtml)


if __name__ == '__main__':
    unittest.main()
