from threading import Thread, Lock
from time import sleep
from collections import deque

try:
    # Python3
    from queue import Queue
except ImportError:
    # Python2
    from Queue import Queue
 
class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super(Worker, self).__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return # END OF THREAD
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super(StoppableWorker, self).__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


def download(item):
    return item # mock

def resize(item):
    return item # mock

def upload(item):
    return item # mock


if __name__ == '__main__':
#     download_queue = MyQueue()
#     resize_queue = MyQueue()
#     upload_queue = MyQueue()
#     done_queue = MyQueue()
#     threads = [
#         Worker(download, download_queue, resize_queue),
#         Worker(resize, resize_queue, upload_queue),
#         Worker(upload, upload_queue, done_queue),
#     ]
# 
#     count = 1000
#     for t in threads:
#         t.start()
#     for _ in range(count):
#         download_queue.put(object())
# 
#     while len(done_queue.items) < count:
#         print('Wait...')
#         sleep(1)
# 
#     processed = len(done_queue.items)
#     polled = sum(t.polled_count for t in threads)
#     print('Processed %(processed)s items ' \
#           'after polling %(polled)s times' % \
#           {'processed': processed, 'polled': polled})

    print('----------------------------')
    download_queue = ClosableQueue()
    resize_queue = ClosableQueue()
    upload_queue = ClosableQueue()
    done_queue = ClosableQueue()
    threads = [
        StoppableWorker(download, download_queue, resize_queue),
        StoppableWorker(resize, resize_queue, upload_queue),
        StoppableWorker(upload, upload_queue, done_queue),
    ]

    count = 1000
    for t in threads:
        t.start()
    for _ in range(count):
        download_queue.put(object())

    def join_queue(queue):
        queue.close()
        queue.join()
    join_queue(download_queue)
    join_queue(resize_queue)
    join_queue(upload_queue)

    print('%s items finished' % done_queue.qsize())

    join_queue(done_queue)
