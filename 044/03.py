import pickle
import copyreg

state_path = 'game_state.bin'

class GameState(object):
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic

def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        del kwargs['lives']
    return GameState(**kwargs)

def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)

copyreg.pickle(GameState, pickle_game_state)

if __name__ == '__main__':
    with open(state_path, 'rb') as f:
        state_after = pickle.load(f)
        print('Read :', state_after.__dict__)
