#!/usr/bin/python

def dummy_method():
    for i in range(1, 40):
        print '.',
    print '-'

def main():
    print 'Running dummy example...'
    from micropeers import reactor
    for i in range(1, 20):
        reactor.add_peer(dummy_method)
    reactor.run()
    print '::all pears exited'

if __name__ == "__main__":
    main()

