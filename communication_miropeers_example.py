#!/usr/bin/python
from micropeers import reactor

class CommunicationFirst(reactor.BasePeer):
    def run(self):
        for i in range(1, 40):
            print '.',
        print ''
        self.send_message(destination_id = 'second_*', method = 'start')
        self.exit()

class CommunicationSecond(reactor.BasePeer):
    def start(self, msg, sender):
        for i in range(1, 40):
            print '*',
        print ''
        self.exit()

def main():
    r = reactor.Reactor()
    r.add_peer(peer_class = CommunicationSecond, id = 'second')
    r.add_peer(peer_class = CommunicationFirst, id = 'first')
    r.run()
    print '::all pears exited'

if __name__ == "__main__":
    main()

