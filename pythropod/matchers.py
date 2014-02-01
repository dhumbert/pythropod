import re
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
        content = data.content
        if 'text' not in self.options:
            raise Exception("Missing text to test for")

        case_sensitive = True if 'case_sensitive' not in self.options else self.options['case_sensitive']

        text = self.options['text']
        if not case_sensitive:
            text = text.lower()

        content = self._parse(content)

        data_text = content.get_text()
        if not case_sensitive:
            data_text = data_text.lower()

        if text not in data_text:
            raise NoMatchError("Text {0} was not found".format(text))


class ElementMatcher(Matcher):
    def match(self, data):
        content = data.content
        content = self._parse(content)

        args = {}
        if 'tag' in self.options:
            args['name'] = self.options['tag']

        if 'id' in self.options:
            args['id'] = self.options['id']

        if 'class' in self.options:
            args['class_'] = self.options['class']

        if 'text' in self.options:
            if 'regex' in self.options and self.options['regex']:
                args['text'] = re.compile(self.options['text'])
            else:
                args['text'] = self.options['text']

        found = content.find(**args)

        if not found:
            raise NoMatchError("Element not found")


class ResponseCodeMatcher(Matcher):
    def __init__(self, options, response_code=200):
        super(Matcher, self).__init__()
        self.response_code = response_code

    def match(self, data):
        if data.status_code != self.response_code:
            raise NoMatchError("Response code {} does not match expected {}".format(data.status_code, self.response_code))

