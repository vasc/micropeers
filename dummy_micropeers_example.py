#!/usr/bin/python

from micropeers import reactor
    
class Dummy(reactor.BasePeer):
    def run(self):
        for i in range(1, 40):
            print '.',
        print '-'
        self.exit()

def main():
    print 'Running dummy example...'
    r = reactor.Reactor()
    for i in range(1, 20):
        r.add_peer(Dummy)
    r.run()
    print '::all pears exited'

if __name__ == "__main__":
    main()

