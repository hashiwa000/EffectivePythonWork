from threading import Thread

try:
    # Python3
    from queue import Queue
except ImportError:
    # Python2
    from Queue import Queue
    
queue = Queue()

def consumer():
    print('Consumer waiting')
    queue.get()
    print('Consumer done')


if __name__ == '__main__':
    thread = Thread(target=consumer)
    thread.start()

    print('Producer putting')
    queue.put(object())
    thread.join()
    print('Producer done')


