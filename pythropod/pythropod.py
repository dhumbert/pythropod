import matchers
import grequests


class TestFailure(Exception):
    pass


class Pythropod(object):
    def __init__(self, options, callback, pool, request=None):
        self.url = options['url']
        self.test_id = options['id']
        
        if request:
            self.request = request
        else:
            self.request = self._request

        self.callback = callback
        self.pool = pool

        self.matcher = {
            'text': matchers.TextMatcher(options),
            'element': matchers.ElementMatcher(options)
        }[options['type']]

    def run(self):
        try:
            self.request(self.url, self.run_test, self.pool)
        except Exception, e:
            self.callback({
                'id': self.test_id,
                'url': self.url,
                'passed': False,
                'msg': e.message,
                })

    def run_test(self, data, **kwargs):
        test_data = {
            'id': self.test_id,
            'url': self.url,
            'passed': True,
            'msg': "Test Passed",
        }

        try:
            self.matcher.match(data.content)
        except Exception as e:
            test_data['passed'] = False
            test_data['msg'] = e.message

        self.callback(test_data)
    
    def _request(self, url, callback, pool):
        req = grequests.get(url, hooks=dict(response=callback), verify=False)
        grequests.send(req, pool)

