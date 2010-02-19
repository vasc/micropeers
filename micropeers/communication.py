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
                reactor.add_task(target=getattr(peer, method), args=(msg, sender), name="send_message")

    def request(reactor, peer, method):
        '''When a request a message is sent but a return value is expected
the function will block waiting for the answer'''
        raise NotImplementedError
