import threading

reactor = {'peers': [], 'peers_id': {}}

class BasePeer:
    def run(self):
        pass
    _id_ = ""
    _base_id_ = ""

def add_peer(peer_class, base_id='default', args=()):
    global reactor
    if not(base_id in reactor['peers_id']):
        reactor['peers_id'][base_id] = 0
    full_id = base_id + '_' + str(reactor['peers_id'][base_id])
    reactor['peers_id'][base_id] += 1
    print peer_class
    peer_class = peer_class()
    peer_class._id_ = full_id
    peer_class.__base_id__ = base_id
    peer = { 'class': peer_class, 'args': args}
    reactor['peers'].append(peer)


def run():
    global reactor
    threads = []
    for peer in reactor['peers']:
        t = threading.Thread(target = peer['class'].run, name = peer['class']._id_, args = peer['args'])
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

