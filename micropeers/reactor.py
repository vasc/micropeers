import threading, sys
from communication import BaseCommunication
from Queue import Queue
import taskmanager


class BasePeer(BaseCommunication):
    _id_ = None
    _base_id_ = None

    def run(self):
        pass

    def exit(self):
        self.__reactor__.exit_peer(self)


class Reactor:
    peers = None
    peers_id = None
    task_manager = None
    task_manager_thread = None
    exit_event = None
    #clock = 0
   
    def __init__(self, concurrent_tasks_limit = 1, allowed_tasks_limit = sys.maxint):
        self.peers = []
        self.peers_id = {}
        self.task_manager = taskmanager.Manager(concurrent_tasks_limit, allowed_tasks_limit)
        self.exit_event = threading.Event()

    def add_peer(self, peer_class, base_id='default', args=(), id=''):
        if id == '':
            if not(base_id in self.peers_id):
                self.peers_id[base_id] = 0
            full_id = base_id + '_' + str(self.peers_id[base_id])
            self.peers_id[base_id] += 1
        else:
            base_id = id
            full_id = id
        peer = peer_class()
        peer._id_ = full_id
        peer.__base_id__ = base_id
        peer.__reactor__ = self
        self.peers.append(peer)
        self.add_task(taskmanager.Task(peer.run, *args))#, name = peer._id_)

    def exit_peer(self, peer):
        self.peers.remove(peer)
        if len(self.peers) == 0:
            self.exit_event.set()

    def run(self):
        if len(self.peers) == 0:
            return
        t = threading.Thread(target = self.task_manager.task_pool, name = '_task_pool')
        t.setDaemon(True)
        self.task_manager_thread = t
        t.start()
        self.exit_event.wait()

    def send_message(self, dest, msg, sender):
        task = taskmanager.Message(dest, msg, sender)
        self.task_manager.add_task(task)
        
    def make_request(self, dest, *args):
        task = taskmanager.Request(dest, *args)
        self.task_manager.create_request(task.request_id)
        self.task_manager.add_task(task)
        self.task_manager.requests[task.request_id]['event'].wait()
        value = requests[task.request_id]['value']
        del requests[task.request_id]
        return value

    def add_task(self, task):
        self.task_manager.add_task(task)

    

