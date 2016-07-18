# -*- coding: utf-8 -*-

class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s.' % name
        setattr(self, name, value)
        return value

class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        # return super().__getattr__(name) # for Python3
        return super(LoggingLazyDB, self).__getattr__(name) # for Python2

class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            # return super().__getattribute__(name) # for Python3
            return super(ValidatingDB, self).__getattribute__(name) # for Python2
        except AttributeError:
            value = 'Value for %s.' % name
            setattr(self, name, value)
            return value

if __name__ == '__main__':
    # data = LazyDB()
    data = LoggingLazyDB()
    print('Before: ', data.__dict__)
    print('foo   : ', data.foo)
    print('foo   : ', data.foo)
    print('After : ', data.__dict__)

    data = ValidatingDB()
    print('Before: ', data.__dict__)
    print('foo   : ', data.foo)
    print('foo   : ', data.foo)
    print('After : ', data.__dict__)


