#!/usr/bin/python
from micropeers import reactor

class RequestFirst(reactor.BasePeer):
    def run(self):
        print '1. Before first request :1'
        second = self.communication.get_peer_proxy('second')
        status = second.answer_request()
        #status = self.request(peer_id = 'second', method = 'answer_request')
        print '6. First request status %s :1' % status
        self.exit()
    
    def answer_request(self):
        print '4. Executing second request :1'
        return 'done'

class RequestSecond(reactor.BasePeer):
    def answer_request(self):
        print '2. Executing first request :2'
        print '3. Before second request :2'
        #status = self.request(peer_id = 'first', method = 'answer_request')
        first = self.communication.get_peer_proxy('first')
        status = first.answer_request()
        print '5. Second request status %s :2' % status
        self.exit()
        return 'done'

def main():
    r = reactor.Reactor()
    r.add_peer(RequestSecond(), id = 'second')
    r.add_peer(RequestFirst(), id = 'first')
    r.run()
    print '::all pears exited'

if __name__ == "__main__":
    main()

