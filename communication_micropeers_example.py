#!/usr/bin/python
from micropeers import reactor

class CommunicationFirst(reactor.BasePeer):
    def run(self):
        for i in range(1, 40):
            print '.',
        print ''
        self.communication.get_peer_proxy('second', sync=False).start()
        #self.send_message(destination_id = 'second_*', method = 'start')
        self.exit()

class CommunicationSecond(reactor.BasePeer):
    def start(self):
        for i in range(1, 40):
            print '*',
        print ''
        self.exit()

def main():
    r = reactor.Reactor()
    r.add_peer(CommunicationSecond(), id = 'second')
    r.add_peer(CommunicationFirst(), id = 'first')
    r.run()
    print '::all pears exited'

if __name__ == "__main__":
    main()

