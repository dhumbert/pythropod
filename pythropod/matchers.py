from bs4 import BeautifulSoup


class NoMatchError(Exception):
    pass


class Matcher(object):
    def __init__(self, options):
        self.options = options

    def _parse(self, data):
        return BeautifulSoup(data)

    def match(self, data):
        raise NotImplementedError()


class TextMatcher(Matcher):
    def match(self, data):
        if 'text' not in self.options:
            raise Exception("Missing text to test for")

        text = self.options['text']
        data = self._parse(data)
        dataText = data.get_text()

        if text not in dataText:
            raise NoMatchError("Text {0} was not found".format(text))


class ElementMatcher(Matcher):
    pass
