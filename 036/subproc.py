import subprocess

from time import sleep
from os import environ, urandom

class Counter(object):
    def __init__(self):
        self.count = 0

    @property
    def next(self):
        self.count += 1
        return self.count

def run_openssl(data):
    env = environ.copy()
    # env['password'] = b'\xe24U\n\xdo0l3S\x11'
    env['password'] = b'1234'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc

def run_md5(input_stdin):
    proc = subprocess.Popen(
        # ['md5'],
        ['md5sum'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)
    return proc

if __name__ == '__main__':
    c = Counter()


    print('--- %03d ---' % c.next)
    proc = subprocess.Popen(
        ['echo', 'Hello from the child!'],
        # ['sleep', '60'],
        stdout=subprocess.PIPE)

    out, err = proc.communicate()
    print(out.decode('utf-8'))


    print('--- %03d ---' % c.next)
    proc = subprocess.Popen(['sleep', '0.3'])
    while proc.poll() is None:
        print('Working...')
        sleep(0.1)


    print('--- %03d ---' % c.next)
    procs = []
    for _ in range(3):
        data = urandom(10)
        proc = run_openssl(data)
        procs.append(proc)

    for proc in procs:
        out, err = proc.communicate()
        print(out[-10:])


    print('--- %03d ---' % c.next)
    input_procs = []
    hash_procs = []
    for _ in range(3):
        data = urandom(10)
        proc = run_openssl(data)
        input_procs.append(proc)
        hash_proc = run_md5(proc.stdout)
        hash_procs.append(hash_proc)

    for proc in input_procs:
        proc.communicate()
    for proc in hash_procs:
        out, err = proc.communicate()
        print(out.strip())


