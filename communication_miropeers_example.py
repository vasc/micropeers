#!/usr/bin/python

from micropeers import communication, reactor

class CommunicationFirst:
    def __init__(self):
        for i in range(1, 40):
            print '.',
        print ''
        communication.send_message(dest = 'second.run')

class CommunicationSecond:
    def run(self, msg, sender):
        for i in range(1, 40):
            print '*',
        print ''

def main():
    from micropeers import reactor
    reactor.add_peer(peer_function = CommunicationSecond, id = 'second')
    reactor.add_peer(peer_function = CommunicationFirst, id = 'first')
    reactor.run()
    print '::all pears exited'

if __name__ == "__main__":
    main()

