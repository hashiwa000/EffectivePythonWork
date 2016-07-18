# -*- coding: utf-8 -*-

class Field(object):
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

class DatabaseRow(object):
    __metaclass__ = Meta

class BetterCustomer(DatabaseRow):
    # class attribute
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


if __name__ == '__main__':
    foo = BetterCustomer()
    print 'Before: %(first_name)r %(dict)s' % \
        {'first_name': foo.first_name, 'dict': foo.__dict__}
    foo.first_name = 'Euclid'
    print 'Before: %(first_name)r %(dict)s' % \
        {'first_name': foo.first_name, 'dict': foo.__dict__}



