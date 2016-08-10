from time import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

numbers = [(1963309, 2265973),
           (2030677, 3814172),
           (1551645, 2229620),
           (2039045, 2020802),
          ]

def do_single():
    start = time()
    result = list(map(gcd, numbers))
    end = time()
    print('Took %.3f seconds' % (end - start))

def do_multi_thread():
    start = time()
    pool = ThreadPoolExecutor(max_workers=2)
    result = list(pool.map(gcd, numbers))
    end = time()
    print('Took %.3f seconds' % (end - start))

def do_multi_process():
    start = time()
    pool = ProcessPoolExecutor(max_workers=2)
    result = list(pool.map(gcd, numbers))
    end = time()
    print('Took %.3f seconds' % (end - start))

if __name__ == '__main__':
    do_single()
    do_multi_thread()
    do_multi_process()

