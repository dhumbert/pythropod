import unittest
from pythropod.matchers import TextMatcher, ElementMatcher, NoMatchError


dummyHtml = """
        <html>
            <body>
                Lorem ipsum dolor sit amet.
            </body>
        </html>
        """


class TextMatcherTestCase(unittest.TestCase):
    def test_total_failure(self):
        m = TextMatcher({'text': 'notintextatall'})
        self.assertRaises(NoMatchError, m.match, dummyHtml)

    def test_case_sensitive_failure(self):
        m = TextMatcher({'text': 'lorem'})
        self.assertRaises(NoMatchError, m.match, dummyHtml)

    def test_case_sensitive_success(self):
        m = TextMatcher({'text': 'Lorem'})
        try:
            m.match(dummyHtml)
        except NoMatchError:
            self.fail("match() shouldn't have failed on case-sensitive search")

    def test_case_insensitive_success(self):
        m = TextMatcher({'text': 'lorem', 'case_sensitive': False})
        try:
            m.match(dummyHtml)
        except NoMatchError:
            self.fail("match() shouldn't have failed on case-insensitive search")


class ElementMatcherTestCase(unittest.TestCase):
    def test_tag_failure(self):
        m = ElementMatcher({'tag': 'blink'})
        self.assertRaises(NoMatchError, m.match, dummyHtml)


if __name__ == '__main__':
    unittest.main()
