import threading
import re

class SyncProxy:
    def __getattr__(self, name):
        if re.match("[^_]", name):
            def sync_request(self, *args, **kwargs):
                for peer in self.reactor.peers:
                    if self.peer_id == peer._id_:
                        return self.reactor.make_sync_request(dest=getattr(peer, name), args=(args, kwargs))
                raise NameError("Peer not found: %s" % self.peer_id)
            setattr(SyncProxy, name, sync_request)
            return getattr(self, name)
        else:  raise AttributeError, name
   
    def __init__(self, reactor, peer_id):
        self.peer_id = peer_id
        self.reactor = reactor 


class AsyncProxy:
    def __getattr__(self, name):
        if re.match("[^_]", name):
            def async_request(self, *args, **kwargs):
                for peer in self.reactor.peers:
                    if re.search(self.peer_id, peer._id_):
                        self.reactor.make_async_request(dest=getattr(peer, name), args=(args, kwargs))
            setattr(AsyncProxy, name, async_request)
            return getattr(self, name)
        else:  raise AttributeError, name
   
    def __init__(self, reactor, peer_id):
        self.peer_id = peer_id
        self.reactor = reactor

#class BaseCommunication:
#    __reactor__ = None
#
#    class PeerProxy:
#        pass
#
#    def send_message(self, msg = '', destination_id = '.*', method = 'run'):
#        if not self.__reactor__:
#            raise UnboundLocalError
#        reactor = self.__reactor__
#        sender = self._id_
#        for peer in reactor.peers:
#            if re.search(destination_id, peer._id_):
#                reactor.send_message(getattr(peer, method), msg, sender)#, name="send_message")
#
#    def request(self, peer_id, method, **kwargs):
#        if not self.__reactor__:
#            raise UnboundLocalError
#        reactor = self.__reactor__
#        for peer in reactor.peers:
#            if peer_id == peer._id_:
#                return reactor.make_request(dest=getattr(peer, method), **kwargs)
#        return None

