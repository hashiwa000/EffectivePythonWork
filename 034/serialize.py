import json

class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})

class Point2D(Serializable):
    def __init__(self, x, y):
        super(Point2D, self).__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)

class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super(BetterPoint2D, self).__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'BetterPoint2D(%d, %d)' % (self.x, self.y)

class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })


registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable):
    __metaclass__ = Meta

class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super(Vector3D, self).__init__(x, y, z)
        self.x, self.y, self.z, = x, y, z

    def __repr__(self):
        return 'Vector3D(%d, %d, %d)' % (self.x, self.y, self.z)


if __name__ == '__main__':
    point = Point2D(5, 3)
    print 'Object:     ', point
    print 'Serialized: ', point.serialize()

    print '----------------'

    point = BetterPoint2D(5, 3)
    print 'Before:     ', point
    data = point.serialize()
    print 'Serialized: ', data
    after = BetterPoint2D.deserialize(data)
    print 'After:      ', after
    
    print '----------------'

    v3 = Vector3D(10, -7, 3)
    print 'Before:     ', v3
    data = v3.serialize()
    print 'Serialized: ', data
    print 'After:      ', deserialize(data)
    print 'registerd:  ', registry

