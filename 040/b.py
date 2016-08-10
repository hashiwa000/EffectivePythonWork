
def minimize():
    current = yield
    while True:
        value = yield current
        current = min(value, current)


if __name__ == '__main__':
    it = minimize()
    next(it)
    print(it.send(10))
    print(it.send(4))
    print(it.send(22))
    print(it.send(-1))


