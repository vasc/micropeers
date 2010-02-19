import threading
from Queue import Queue
import sys

class Manager:
    #running_tasks = None
    concurrent_tasks_limit = None
    allowed_tasks_limit = None
    task_queue = None
    threads = None

    def __init__(self, concurrent_tasks_limit = 1, allowed_tasks_limit = sys.maxint):
        if not isinstance(concurrent_tasks_limit, (int,long)) or concurrent_tasks_limit < 1:
            concurrent_tasks_limit = 1
        self.running_tasks = []
        self.concurrent_tasks_limit = threading.Semaphore(concurrent_tasks_limit)
        self.allowed_tasks_limit = threading.Semaphore(allowed_tasks_limit)
        self.task_queue = Queue(0)
        self.threads = []

    def task_pool(self):
        while(True):
            self.concurrent_tasks_limit.acquire()
            self.join_finished_threads()
            self.allowed_tasks_limit.acquire()
            task = self.task_queue.get()
            t = threading.Thread(target = self.thread_wrapper, name = task['name'], kwargs = {'target': task['target'], 'args': task['args']})
            t.setDaemon(True)
            self.threads.append(t)
            #running_tasks.append(task)
            t.start()

    def thread_wrapper(self, target, args):
        target(*args)
        self.concurrent_tasks_limit.release()

    def join_finished_threads(self):
        for t in self.threads:
            t.join(0)

    def add_task(self, task):
        self.task_queue.put(task)

    def allow_running_tasks(n = 1):
        for i in range(n):
            self.allowed_tasks_limit.release()

    
