from config import EPSILON, EPSILON_DECAY, EPSILON_MIN, GAMMA, ALPHA, Default_model_path
from modules.environment import Stage
import numpy as np
import json

class Agent:
    def __init__(self, learning=True, epsilon=EPSILON, epsilon_decay=EPSILON_DECAY, epsilon_min=EPSILON_MIN, gamma=GAMMA, alpha=ALPHA):
        self.qtable = {}
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.gamma = gamma
        self.alpha = alpha
        self.action_size = 4
        self.learning = learning

    def get_action(self, vision_key: tuple[str]):
        """get action for a given state"""
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
        for i, (dx, dy) in enumerate(direction):
            next_is_wall = True
            x, y = head[0], head[1]
            while 0 <= x < state.size and 0 <= y < state.size:
                if (x, y) == head:
                    pass
                elif (x, y) in state.snake:
                    if len(vision[i]) == 0 and next_is_wall:
                        vision[i] += "S"
                        break
                    else:
                        vision[i] += "0S"
                elif (x, y) == state.red_apple:
                    vision[i] += "R"
                elif (x, y) in state.green_apples:
                    vision[i] += "G"
                else:
                    next_is_wall = False
                x += dx
                y += dy
            if len(vision[i]) == 0:
                if next_is_wall:
                    vision[i] += "W"
                else:
                    vision[i] += "0"

        if print_vision:
            self.print_vision(state)
        return vision

    def print_vision(self, state: Stage):
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
        print("------------------------")

    def learn(self, old_vision_key: tuple[str], new_vision_key: tuple[str], reward: int, action: int):
        """learn from the experience"""
        if not self.learning:
            return

        if old_vision_key not in self.qtable:
            self.qtable[old_vision_key] = np.zeros(self.action_size)

        if new_vision_key not in self.qtable:
            self.qtable[new_vision_key] = np.zeros(self.action_size)

        old_q_value = self.qtable[old_vision_key][action]
        next_max = np.max(self.qtable[new_vision_key])
        new_q_value = (1 - self.alpha) * old_q_value + self.alpha * (reward + self.gamma * next_max)
        self.qtable[old_vision_key][action] = new_q_value

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, filename=Default_model_path):
        model_data = {
            'qtable': {str(k): v.tolist() for k, v in self.qtable.items()},
            'epsilon': self.epsilon
        }
        with open(filename, 'w') as f:
            json.dump(model_data, f)

    def load_model(self, filename):
        with open(filename, 'r') as f:
            model_data = json.load(f)
        self.qtable = {eval(k): np.array(v) for k, v in model_data['qtable'].items()}
        self.epsilon = model_data['epsilon']
