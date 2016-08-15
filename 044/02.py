import pickle
import copyreg

state_path = 'game_state.bin'

class GameState(object):
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic

def unpickle_game_state(kwargs):
    return GameState(**kwargs)

def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)

copyreg.pickle(GameState, pickle_game_state)

if __name__ == '__main__':
    with open(state_path, 'rb') as f:
        state_after = pickle.load(f)
        print('Read :', state_after.__dict__)

    with open(state_path, 'wb') as f:
        pickle.dump(state_after, f)
        print('Write:', state_after.__dict__)

    with open(state_path, 'rb') as f:
        serialized = f.read()
        print('serialized:', serialized[:25])


