from threading import Thread, Lock
from time import time

class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset=1):
        self.count += offset


class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset=1):
        with self.lock:
            self.count += offset


def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        # Read from sensor
        # ...
        counter.increment()


def run_threads(func, how_many, counter):
    def create_thread(i):
        return Thread(target=func, args=(i, how_many, counter))
    threads = [create_thread(i) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


class Time(object):
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.end = time()
        print('Took %.3f seconds' % (self.end - self.start))


if __name__ == '__main__':
    how_many = 10**5
    counter = Counter()
    with Time():
        run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % 
          (5 * how_many, counter.count))

    counter = LockingCounter()
    with Time():
        run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % 
          (5 * how_many, counter.count))


