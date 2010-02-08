#!/usr/bin/python

from micropeers import comunication

def comunication_first(id):
    for i in range(1..1000):
        print '.',
    print ''
    comunication.send_message({dest: 'second', msg: 'done', type: comunication.single_receiver})

def comunication_second(id):
    comunication.receive_message({sender: 'first', msg: 'done'})
    for i in range(1..1000):
        print '*',
    print ''

def main():
    from micropeers import reactor
    reactor.add_peer({method: comunication_second, id: 'second'})
    reactor.add_peer({method: comunication_first, id: 'first'})
    reactor.run()
    print '::all pears exited'

if __name__ == "main":
    main()