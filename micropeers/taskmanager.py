import threading
from Queue import Queue
import sys
import uuid

class Task:
    name = "default_task_name"
    target = None
    args = None

    def run(self):
        self.return_value = self.target(*self.args)
        return self.return_value

    def __init__(self, target, *args):
       self.target = target
       self.args = args

class Message(Task):
    pass

class Dummy(Task):
    def __init__(self, request_id):
        self.request_id = request_id

class Request(Task):
    def __init__(self, target, *args):
        Task.__init__(self, target, *args)
        self.request_id = uuid.uuid4()

class Manager:
    #running_tasks = None
    concurrent_tasks_limit = None
    allowed_tasks_limit = None
    task_queue = None
    threads = None
    requests = None

    def __init__(self, concurrent_tasks_limit = 1, allowed_tasks_limit = sys.maxint):
        if not isinstance(concurrent_tasks_limit, (int,long)) or concurrent_tasks_limit < 1:
            concurrent_tasks_limit = 1
        #self.running_tasks = []
        self.concurrent_tasks_limit = threading.Semaphore(concurrent_tasks_limit)
        self.allowed_tasks_limit = threading.Semaphore(allowed_tasks_limit)
        self.task_queue = Queue(0)
        self.threads = []
        self.requests = {}

    def task_pool(self):
        while(True):
            self.concurrent_tasks_limit.acquire()
            self.join_finished_threads()
            self.allowed_tasks_limit.acquire()
            task = self.task_queue.get()
            t = threading.Thread(target = self.task_runner, name = task.name, kwargs = {'task': task})
            t.setDaemon(True)
            self.threads.append(t)
            #running_tasks.append(task)
            t.start()

    #def thread_wrapper(self, target, args, request_id = None):
    #    target(*args)
    #    self.concurrent_tasks_limit.release()

    def task_runner(self, task):
        if isinstance(task, Dummy):
            self.requests[task.request_id]['event'].set()
        elif isinstance(task, Request):
            self.requests[task.request_id]['value'] = task.run()
            self.add_task(Dummy(task.request_id))
            self.concurrent_tasks_limit.release()
        elif isinstance(task, Task):
            task.run()
            self.concurrent_tasks_limit.release()
        else:
            raise Exception()

    def request_return(self, request_id):
        self.requests[request_id]['event'].set()

    def join_finished_threads(self):
        for t in self.threads:
            t.join(0)

    def add_task(self, task):
        self.task_queue.put(task)

    def allow_running_tasks(n = 1):
        for i in range(n):
            self.allowed_tasks_limit.release()

    def create_request(self, id):
        self.requests[id] = {'event': threading.Event(), 'value': None}
        return id






