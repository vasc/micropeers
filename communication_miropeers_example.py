#!/usr/bin/python

from micropeers import communication, reactor

class CommunicationFirst(reactor.BasePeer):
    def run(self):
        for i in range(1, 40):
            print '.',
        print ''
        communication.send_message(peer_id = 'second_*', method = 'start')

class CommunicationSecond(reactor.BasePeer):
    def start(self, msg, sender):
        for i in range(1, 40):
            print '*',
        print ''

def main():
    from micropeers import reactor
    reactor.add_peer(peer_class = CommunicationSecond, id = 'second')
    reactor.add_peer(peer_class = CommunicationFirst, id = 'first')
    reactor.run()
    print '::all pears exited'

if __name__ == "__main__":
    main()

