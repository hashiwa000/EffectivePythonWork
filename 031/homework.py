from weakref import WeakKeyDictionary

class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        print '__get__ %s %s %s' % (self, instance, instance_type)
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        print '__set__ %s %s %s' % (self, instance, value)
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100.')
        self._values[instance] = value

class Homework(object):
    grade = Grade()

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

if __name__ == '__main__':
    first_exam = Exam()
    first_exam.writing_grade = 82
    second_exam = Exam()
    second_exam.writing_grade = 75
    print 'First  %s is right' % first_exam.writing_grade
    print 'Second %s is right' % second_exam.writing_grade
