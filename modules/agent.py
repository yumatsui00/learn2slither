from config import EPSILON, EPSILON_DECAY, EPSILON_MIN, GAMMA, ALPHA
from modules.environment import Stage
import numpy as np


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

    def get_action(self, snake_vision: list[str]):
        """get action for a given state"""
        vision_key = tuple(snake_vision)
        if self.learning and np.random.random() < self.epsilon:
            return np.random.randint(0, self.action_size - 1)
        elif vision_key not in self.qtable:
            self.qtable[vision_key] = np.zeros(self.action_size)
        #return action with highest q value
        return np.argmax(self.qtable[vision_key])

    def look_around(self, state: Stage, print_vision=False):
        """snake looks around in the state and returns its vision"""
        head = state.snake[0]
        vision = [""] * 4
        direction = [(0, 1),(0, -1),(1, 0),(-1, 0)] #right, left, up, down
        vision_max_length = 3
        for i, (dx, dy) in enumerate(direction):
            x, y = head[0], head[1]
            while 0 <= x < state.size and 0 <= y < state.size:
                if (x, y) == head:
                    vision[i] += "H"
                elif (x, y) in state.snake:
                    vision[i] += "S"
                elif (x, y) == state.red_apple:
                    vision[i] += "R"
                elif (x, y) in state.green_apples:
                    vision[i] += "G"
                else:
                    vision[i] += "0"
                x += dx
                y += dy
            vision[i] += "W"

        if print_vision:
            self.print_vision(vision, state)
        return vision

    def print_vision(self, vision: list[str], state: Stage):
        head = state.snake[0]
        for i in range(state.size + 2):
            for j in range(state.size + 2):
                if i != head[0] and j != head[1]:
                    print(" ", end="")
                else:
                    if i == 0 or i == state.size + 1 or j == 0 or j == state.size + 1:
                        print("W", end="")
                    elif (i, j) in state.snake:
                        if (i, j) == head:
                            print("H", end="")
                        else:
                            print("S", end="")
                    elif (i, j) == state.red_apple:
                        print("R", end="")
                    elif (i, j) in state.green_apples:
                        print("G", end="")
                    else:
                        print("0", end="")
            print()

