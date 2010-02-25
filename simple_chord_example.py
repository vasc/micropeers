#!/usr/bin/python

from micropeers import reactor
from micropeers.taskmanager import DelayError
import hashlib
import struct



def delay(func):
    def f(*args, **kwargs):
        if not args[0].ready:
            raise DelayError()
        return func(*args, **kwargs)
    return f
 
class Chord(reactor.BasePeer):
    id = None
    pos = None
    storage = {}
    successor = None
    m = None
    ready = False


    def get_pos(self, key):
        h = hashlib.sha1()
        h.update(key)
        return struct.unpack('16xI', h.digest())[0] & (2**Chord.m)-1

    def test_key(self, key):
        mypos = self.get_pos(self.id)
        nextpos = self.get_pos(self.successor)
        if nextpos <= mypos: nextpos += 2 ** Chord.m
        keypos = self.get_pos(key)
        if keypos < mypos: keypos += 2 ** Chord.m
        return keypos < nextpos

    def run(self, own_id, connection_id = None):
        self.id = own_id
        #self.pos = self.get_pos()
        if connection_id == None:
            self.successor = own_id
        else:
            self.connect(connection_id)
        self.ready = True

    def connect(self, connection_id):
        connected = False
        while not connected:
            res_lookup = {'success': False, 'previous': None, 'next': connection_id}
            while(not(res_lookup['success'])):
                res_lookup = self.communication.get_peer_proxy(res_lookup['next']).lookup(self.id)
            self.successor = res_lookup['next']
            if self.communication.get_peer_proxy(res_lookup['previous']).commit_successor(self.id, res_lookup['next']):
                connected = True
            else:
                connection_id = res_lookup['previous']
        
    @delay
    def lookup(self, key):
        value = None
        test = self.test_key(key)
        if test and key in self.storage: value = self.storage[key]
        return {'success': test, 'previous': self.id, 'next': self.successor, 'value': value}

    @delay
    def store(self, key, value):
        test = self.test_key(key)
        if test: self.storage[key] = value
        return test

    @delay
    def commit_successor(self, new_successor, old_successor):
        """When the new successor decides it's time to commit calls
           this method to make sure the current node state is still
           stable
        """
        if self.successor == old_successor:
            self.successor = new_successor
            return True
        else:
            return False

def main():
    Chord.m = 7
    r = reactor.Reactor()
    r.add_peer(Chord(), id = 'peer1', args = ("peer1",))
    r.add_peer(Chord(), id = 'peer2', args = ("peer2", "peer1"))
    r.run()
    print '::all pears exited'

if __name__ == '__main__':
    main()
