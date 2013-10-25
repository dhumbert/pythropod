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

        case_sensitive = True if 'case_sensitive' not in self.options else self.options['case_sensitive']

        text = self.options['text']
        if not case_sensitive:
            text = text.lower()

        data = self._parse(data)

        data_text = data.get_text()
        if not case_sensitive:
            data_text = data_text.lower()

        if text not in data_text:
            raise NoMatchError("Text {0} was not found".format(text))


class ElementMatcher(Matcher):
    def match(self, data):
        data = self._parse(data)

        elems = set([])
        if 'tag' in self.options:
            for e in data.find_all(self.options['tag']):
                elems.add(e)

        if not len(elems):
            raise NoMatchError("Element not found")