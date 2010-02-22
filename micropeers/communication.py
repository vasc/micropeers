import threading
import re


class BaseCommunication():
    __reactor__ = None

    def send_message(self, msg = '', destination_id = '.*', method = 'run'):
        if not self.__reactor__:
            raise UnboundLocalError
        reactor = self.__reactor__
        sender = self._id_
        for peer in reactor.peers:
            if re.search(destination_id, peer._id_):
                reactor.send_message(getattr(peer, method), msg, sender)#, name="send_message")

    def request(reactor, peer, method):
        for peer in reactor.peers:
            if re.search(destination_id, peer._id_):
                return reactor.make_request(target=getattr(peer, method), args=(msg, sender), name="request")
        return None
