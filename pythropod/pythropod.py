import client
import matchers


class TestFailure(Exception):
    pass


class Pythropod(object):
    def __init__(self, options, request=client.request):
        # twisted requires URL to be str, not unicode
        self.url = str(options['url'])
        self.request = request

        self.matcher = {
            'text': matchers.TextMatcher(options),
            'element': matchers.ElementMatcher(options)
        }[options['type']]

    def run(self):
        self.request(self.url, self.run_test)

    def run_test(self, data):
        try:
            self.matcher.match(data)
        except matchers.NoMatchError as e:
            print e

