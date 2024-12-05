from config import EPSILON, EPSILON_DECAY, EPSILON_MIN, GAMMA, ALPHA

class Agent:
    def __init__(self, learning=True):
        self.qtable = {}
        self.epsilon = EPSILON
        self.epsilon_decay = EPSILON_DECAY
        self.epsilon_min = EPSILON_MIN
        self.gamma = GAMMA
        self.alpha = ALPHA
        self.action_size = 4
        self.learning = learning

    