import unittest
from pythropod.matchers import TextMatcher, ElementMatcher, NoMatchError


dummyHtml = """
        <html>
            <body>
                <h1 id="realId">Hello, world</h1>
                <p id="anotherRealId" class="realClass">Lorem ipsum dolor sit amet.</p>
                <div class="multiClass1 multiClass2">something</div>
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

    def test_tag_success(self):
        m = ElementMatcher({'tag': 'h1'})
        try:
            m.match(dummyHtml)
        except NoMatchError:
            self.fail("match() shouldn't have failed on element search")

    def test_id_failure(self):
        m = ElementMatcher({'id': 'fakeId'})
        self.assertRaises(NoMatchError, m.match, dummyHtml)

    def test_id_success(self):
        m = ElementMatcher({'id': 'realId'})
        try:
            m.match(dummyHtml)
        except NoMatchError:
            self.fail("match() shouldn't have failed on element id search")

    def test_tag_and_id_failure(self):
        m = ElementMatcher({'tag': 'h1', 'id': 'anotherRealId'})
        self.assertRaises(NoMatchError, m.match, dummyHtml)

    def test_tag_and_id_success(self):
        m = ElementMatcher({'tag': 'h1', 'id': 'realId'})
        try:
            m.match(dummyHtml)
        except NoMatchError:
            self.fail("match() shouldn't have failed on tag+id search")

    def test_class_failure(self):
        m = ElementMatcher({'tag': 'p', 'class': 'fakeClass'})
        self.assertRaises(NoMatchError, m.match, dummyHtml)

    def test_class_success(self):
        m = ElementMatcher({'tag': 'p', 'class': 'realClass'})
        try:
            m.match(dummyHtml)
        except NoMatchError:
            self.fail("match() shouldn't have failed on tag+class search")

    def test_multiple_class_success(self):
        m = ElementMatcher({'tag': 'div', 'class': 'multiClass1'})
        try:
            m.match(dummyHtml)
        except NoMatchError:
            self.fail("match() shouldn't have failed on multi-class search")


if __name__ == '__main__':
    unittest.main()
