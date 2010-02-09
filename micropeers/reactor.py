import threading

reactor = {'peers': [], 'peers_id': {}}

def add_peer(peer_function, id='default', args=()):
    global reactor
    if not(id in reactor['peers_id']):
        reactor['peers_id'][id] = 0
    full_id = id + '_' + str(reactor['peers_id'][id])
    reactor['peers_id'][id] += 1
    peer = { 'function': peer_function, 'id': full_id, 'base_id': id, 'args': args}
    reactor['peers'].append(peer)


def run():
    global reactor
    threads = []
    for peer in reactor['peers']:
        t = threading.Thread(target = peer['function'], name = peer['id'], args = peer['args'])
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

