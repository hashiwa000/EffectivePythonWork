import logging

#logging.basicConfig()
LOG = logging.getLogger(__name__)
# LOG.setLevel(logging.DEBUG)

def normalize(numbers):
    total = sum(numbers)
    LOG.debug('total = %s', total)
    result = []
    for value in numbers:
        percent = value * 100.0 / total
        result.append(percent)
    LOG.debug('result = %s', result)
    return result


def normalize_copy(numbers):
    numbers = list(numbers)
    total = sum(numbers)
    LOG.debug('total = %s', total)
    result = []
    for value in numbers:
        percent = value * 100.0 / total
        result.append(percent)
    LOG.debug('result = %s', result)
    return result


def read_visits(data_path='./my_numbers.txt'):
    with open(data_path) as f:
        for line in f:
            yield int(line)


class ReadVisits(object):
    def __init__(self, data_path='./my_numbers.txt'):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

