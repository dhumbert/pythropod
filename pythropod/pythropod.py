import client, matchers


class TestFailure(Exception):
    pass


class Pythropod(object):
    def __init__(self, options, request=client.request):
        # twisted requires URL to be str, not unicode
        self.url = str(options['url'])
        self.request = request

        if options['type'] == 'text':
            self.matcher = matchers.TextMatcher(options)
        else:
            self.matcher = matchers.ElementMatcher(options)

    def run(self):
        self.request(self.url, self.runTest)

    def runTest(self, data):
        try:
            result = self.matcher.match(data)
        except matchers.NoMatchError as e:
            print e

