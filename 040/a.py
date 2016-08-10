def my_coroutine():
    while True:
        received = yield
        print('Received: %s' % received)

it = my_coroutine()
next(it)
it.send('First')
it.send('Second')

