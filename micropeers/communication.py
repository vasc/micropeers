from micropeers import reactor
import threading
import re

#must have a indirection mechanism so that only the main thread starts other threads
#necessary for clarification and cross network requests
def send_message(msg = '', peer_id = '.*', method = 'run'):
    peers = reactor.reactor['peers']
    sender = threading.current_thread().name
    for peer in peers:
        if re.search(peer_id, peer._id_):
            reactor.thread_wrapper(getattr(peer, method), (msg, sender))


def request(peer, method):
    '''In a request a message is sent but a return value is expected
the function will block waiting for the answer'''
    raise NotImplementedError

