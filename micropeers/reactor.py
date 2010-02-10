import threading, sys
from Queue import Queue

reactor = {'peers': [], 'peers_id': {}, 'task_queue': Queue(0), 'clock': 0}

sync = {'thread_limit_sem': threading.Semaphore(1), 'threads': [], 'exit_cond': threading.Condition()}

class BasePeer:
    _id_ = ""
    _base_id_ = ""

    def run(self):
        pass

    def exit(self):
        exit_peer(self)


def add_peer(peer_class, base_id='default', args=(), id=''):
    if id == '':
        if not(base_id in reactor['peers_id']):
            reactor['peers_id'][base_id] = 0
        full_id = base_id + '_' + str(reactor['peers_id'][base_id])
        reactor['peers_id'][base_id] += 1
    else:
        base_id = id
        full_id = id
    peer = peer_class()
    peer._id_ = full_id
    peer.__base_id__ = base_id
    reactor['peers'].append(peer)
    add_task(target = peer.run, args = args, name = peer._id_)


def exit_peer(peer):
    reactor['peers'].remove(peer)
    if len(reactor['peers']) == 0:
        sync['exit_cond'].acquire()
        sync['exit_cond'].notify()
        sync['exit_cond'].release()


def run():
    if len(reactor['peers']) == 0:
        return
    threads = sync['threads']
    t = threading.Thread(target = task_pool, name = '_task_pool')
    t.setDaemon(True)
    threads.append(t)
    t.start()
    sync['exit_cond'].acquire()
    sync['exit_cond'].wait()


def task_pool():
    threads = sync['threads']
    while(True):
        sync['thread_limit_sem'].acquire()
        task = reactor['task_queue'].get()
        t = threading.Thread(target = thread_wrapper, name = task['name'], kwargs = {'target': task['target'], 'args': task['args']})
        t.setDaemon(True)
        threads.append(t)
        t.start()


def add_task(target, args, name, clock = reactor['clock']):
    reactor['task_queue'].put({'target': target, 'args': args, 'name': name, 'clock': clock})


def thread_wrapper(target, args):
    target(*args)
    sync['thread_limit_sem'].release()

