#!/usr/bin/python

from micropeers import reactor
    
class Dummy(reactor.BasePeer):
    def run(self):
        for i in range(1, 40):
            print '.',
        print '-'

def main():
    print 'Running dummy example...'
    for i in range(1, 20):
        reactor.add_peer(Dummy)
    reactor.run()
    print '::all pears exited'

if __name__ == "__main__":
    main()

