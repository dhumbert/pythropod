from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent


def request(url, callback):
    """Initiate an HTTP request and call callback with returned data"""
    agent = Agent(reactor)
    d = agent.request('GET', url)
    d.addCallbacks(_cb_response, _eb_response, callbackArgs=[callback])
    d.addBoth(_stop)
    reactor.run()


class Midwife(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.data = ""

    def dataReceived(self, bytes):
        self.data += bytes

    def connectionLost(self, reason):
        self.finished.callback(self.data)


def _cb_response(response, callback):
    finished = Deferred()
    finished.addCallback(callback)
    response.deliverBody(Midwife(finished))
    return finished


def _eb_response(failure):
    print failure


def _stop(response):
    reactor.stop()
