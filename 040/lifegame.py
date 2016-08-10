from collections import namedtuple
import logging

def get_logger(name, level=logging.WARNING):
    FORMAT = '%(asctime)-15s %(levelname)s %(funcName)s %(message)s'
    logging.basicConfig(format=FORMAT, level=level)
    return logging.getLogger(name)

# LOG = get_logger(name=__name__, level=logging.INFO)
LOG = get_logger(name=__name__)

ALIVE = '*'
EMPTY = '-'

TICK = object()

Query = namedtuple('Query', ('y', 'x'))
Transition = namedtuple('Transition', ('y', 'x', 'state'))

def count_neighbors(y, x):
    """ Count the number of live neighbors. """
    n_ = yield Query(y + 1, x    ) # North
    ne = yield Query(y + 1, x + 1) # North East
    e_ = yield Query(y    , x + 1) # East
    se = yield Query(y - 1, x + 1) # South East
    s_ = yield Query(y - 1, x    ) # South
    sw = yield Query(y - 1, x - 1) # South West
    w_ = yield Query(y    , x - 1) # West
    nw = yield Query(y + 1, x - 1) # North West
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


def game_logic(state, neighbors):
    """ Decide ALIVE or EMPTY. """
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state


def step_cell(y, x):
    """ Process one step for the cell. """
    state = yield Query(y, x)
    LOG.info('state = %s', ('ALIVE' if state == ALIVE else 'EMPTY'))
    neighbors = yield from count_neighbors(y, x)
    LOG.info('neighbors = %s', neighbors)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


def simulate(height, width):
    """ Simulate LifeGame. """
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny


class Grid(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        canvas = ''
        for row in self.rows:
            for cell in row:
                canvas += cell
            canvas += '\n'
        return canvas

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state


#### test functions ####

def testQueue():
    it = count_neighbors(10, 5)
    q1 = next(it)
    print('1st yield: ', q1)
    q2 = it.send(ALIVE)
    print('2nd yield: ', q2)
    q3 = it.send(ALIVE)
    print('3rd yield: ', q3)
    q4 = it.send(ALIVE)
    print('4th yield: ', q4)
    q5 = it.send(ALIVE)
    print('5th yield: ', q5)
    q6 = it.send(ALIVE)
    print('6th yield: ', q6)
    q7 = it.send(ALIVE)
    print('7th yield: ', q7)
    q8 = it.send(ALIVE)
    print('8th yield: ', q8)
    try:
        it.send(ALIVE)
    except StopIteration as e:
        print ('Count: %s' % e.value)

def testTransition():
    it = step_cell(10, 5)
    q0 = next(it)          # Query of initial state
    print('Me:      ', q0)
    q1 = it.send(ALIVE)    # Send own state (ALIVE) and get Query of neighbor's state
    print('Q1:      ', q1)
    q2 = it.send(ALIVE)    # Send own state (ALIVE) and get Query of neighbor's state
    print('Q2:      ', q2)
    q3 = it.send(ALIVE)    # Send own state (ALIVE) and get Query of neighbor's state
    print('Q3:      ', q3)
    q4 = it.send(ALIVE)    # Send own state (ALIVE) and get Query of neighbor's state
    print('Q4:      ', q4)
    q5 = it.send(ALIVE)    # Send own state (ALIVE) and get Query of neighbor's state
    print('Q5:      ', q5)
    q6 = it.send(ALIVE)    # Send own state (ALIVE) and get Query of neighbor's state
    print('Q6:      ', q6)
    q7 = it.send(ALIVE)    # Send own state (ALIVE) and get Query of neighbor's state
    print('Q7:      ', q7)
    q8 = it.send(ALIVE)    # Send own state (ALIVE) and get Query of neighbor's state
    print('Q8:      ', q8)
    t1 = it.send(EMPTY)
    print('Outcome: ', t1)

def testGrid(n_step=5):
    def make_initial_grid():
        grid = Grid(5, 9)
        grid.assign(0, 3, ALIVE)
        grid.assign(1, 4, ALIVE)
        grid.assign(2, 2, ALIVE)
        grid.assign(2, 3, ALIVE)
        grid.assign(2, 4, ALIVE)
        return grid
    grid = make_initial_grid()
    sim = simulate(grid.height, grid.width)
    for i in range(n_step):
        print('%05d' % i)
        print(grid)
        grid = live_a_generation(grid, sim)

if __name__ == '__main__':
    # testQueue()
    # testTransition()
    testGrid(100)
    
    
