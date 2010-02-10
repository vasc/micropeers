import threading

reactor = {'peers': [], 'peers_id': {}}

class BasePeer:
    def run(self):
        pass
    _id_ = ""
    _base_id_ = ""


def add_peer(peer_class, base_id='default', args=(), id=''):
    global reactor
    if id == '':
        if not(base_id in reactor['peers_id']):
            reactor['peers_id'][base_id] = 0
        full_id = base_id + '_' + str(reactor['peers_id'][base_id])
        reactor['peers_id'][base_id] += 1
    else:
        base_id = id
        full_id = id
    peer_class = peer_class()
    peer_class._id_ = full_id
    peer_class.__base_id__ = base_id
    peer = { 'class': peer_class, 'args': args}
    reactor['peers'].append(peer)


def run():
    global reactor
    threads = []
    for peer in reactor['peers']:
        t = threading.Thread(target = thread_wrapper, name = peer['class']._id_, kwargs = {'target': peer['class'].run, 'args': peer['args']})
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def thread_wrapper(target, args):
    #future thread wrapper code
    target(*args)

