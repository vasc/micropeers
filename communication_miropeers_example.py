#!/usr/bin/python

from micropeers import communication

def communication_first(id):
    for i in range(1..1000):
        print '.',
    print ''
    communication.send_message({dest: 'second', msg: 'done', type: communication.single_receiver})

def communication_second(id):
    communication.receive_message({sender: 'first', msg: 'done'})
    for i in range(1..1000):
        print '*',
    print ''

def main():
    from micropeers import reactor
    reactor.add_peer({method: communication_second, id: 'second'})
    reactor.add_peer({method: communication_first, id: 'first'})
    reactor.run()
    print '::all pears exited'

if __name__ == "main":
    main()

