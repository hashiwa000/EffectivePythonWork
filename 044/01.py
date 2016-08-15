import pickle

state_path = 'game_state.bin'

class GameState(object):
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points

if __name__ == '__main__':
    state = GameState()
    state.level += 1
    state.lives -= 1

    print('Write:', state.__dict__)

    with open(state_path, 'wb') as f:
        pickle.dump(state, f)

    with open(state_path, 'rb') as f:
        serialized = f.read()
        print('serialized:', serialized[:25])


