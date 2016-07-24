from time import time, sleep
from threading import Thread
from select import select
from socket import socket

class Time(object):
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.end = time()
        print('Took %.3f seconds' % (self.end - self.start))

def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

class FactorizeThread(Thread):
    def __init__(self, number):
        super(FactorizeThread, self).__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

def slow_systemcall():
    # select([socket()], [], [], 0.1)
    sleep(0.1)

if __name__ == '__main__':
    numbers = [2139079, 1214759, 1516637, 1852285]

    with Time():
        for number in numbers:
            list(factorize(number))

    with Time():
        threads = []
        for number in numbers:
            thread = FactorizeThread(number)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    with Time():
        for _ in range(5):
            slow_systemcall()

    with Time():
        threads = []
        for _ in range(5):
            thread = Thread(target=slow_systemcall)
            thread.start()
            threads.append(thread)

        def compute_helicopter_location(index):
            pass #mock

        for i in range(5):
            compute_helicopter_location(i)
        for thread in threads:
            thread.join()


