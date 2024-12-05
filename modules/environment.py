import numpy as np
import random
import time
from collections import deque
from config import MOVE_PENALTY, GREEN_APPLE_REWARD, RED_APPLE_PENALTY, GAME_OVER_PENALTY, APPROACH_PENALTY, APPROACH_GREEN_APPLE_REWARD, APPROACH_RED_APPLE_PENALTY

class Stage:
    def __init__(self, size):
        self.size = size
        self.red_apple = None
        self.green_apples = []
        self.snake = None
        self.grid = None
        self.reset()

    def reset(self):
        """reset game state"""
        snake_head_x = np.random.randint(1, self.size - 2)
        snake_head_y = np.random.randint(1, self.size - 2)
        # generate snake body
        self.snake = deque([(snake_head_x, snake_head_y)])
        for i in range(2):
            self.snake.append((snake_head_x, snake_head_y + i + 1))

        #generate apples
        self.red_apple = self._generate_apple()
        self.green_apples = [self._generate_apple(), self._generate_apple()]

        #update grid
        self._update_grid()

        #reset score and game over
        self.score = 0
        self.game_over = False
        return self._get_state()


    def _update_grid(self):
        """update grid with snake and apples"""
        self.grid = np.zeros((self.size, self.size))
        for pos in self.snake:
            self.grid[pos] = 1
        self.grid[self.red_apple] = 2
        for pos in self.green_apples:
            self.grid[pos] = 3


    def _get_state(self):
        """get current game state"""
        return self.grid

    def _generate_apple(self):
        """generate a random position for an apple that is not in the snake, and not the same as the apples"""
        while True:
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            if pos in self.snake:
                continue
            if self.red_apple and pos == self.red_apple:
                continue
            if self.green_apples and pos in self.green_apples:
                continue
            return pos

    def step(self, snake, action, snake_vision):
        """step the game forward"""
        direction = [(0, 1),(0, -1),(1, 0),(-1, 0)] #right, left, up, down
        dx, dy = direction[action]

        #move snake
        head = self.snake[0]
        new_head = (head[0] + dx, head[1] + dy)

        #MOVE_PENALTY
        reward = MOVE_PENALTY

        print(snake_vision)
        #collision penalty with wall or snake body
        if (len(snake_vision[0]) == 1 or len(snake_vision[1]) == 1 or len(snake_vision[2]) == 1 or len(snake_vision[3]) == 1):
            print("check point 2")
            reward += GAME_OVER_PENALTY
            self.game_over = True
            return self._get_state(), reward, self.game_over
        elif new_head in self.snake:
            print("check point 3")
            reward += GAME_OVER_PENALTY
            self.game_over = True
            return self._get_state(), reward, self.game_over

        #penalty for approaching snake body
        for segment in list(self.snake)[1:]:
            if abs(new_head[0] - segment[0]) + abs(new_head[1] - segment[1]) == 1:
                reward += APPROACH_PENALTY

        #reward or penalty for approaching green apple or red apple
        for i, vision in enumerate(snake_vision):
            if "G" in vision:
                if i == 0 and new_head[1] == head[1] + 1:
                    reward += APPROACH_GREEN_APPLE_REWARD
                elif i == 1 and new_head[1] == head[1] - 1:
                    reward += APPROACH_GREEN_APPLE_REWARD
                elif i == 2 and new_head[0] == head[0] + 1:
                    reward += APPROACH_GREEN_APPLE_REWARD
                elif i == 3 and new_head[0] == head[0] - 1:
                    reward += APPROACH_GREEN_APPLE_REWARD
            elif "R" in vision:
                if i == 0 and new_head[1] == head[1] + 1:
                    reward += APPROACH_RED_APPLE_PENALTY
                elif i == 1 and new_head[1] == head[1] - 1:
                    reward += APPROACH_RED_APPLE_PENALTY
                elif i == 2 and new_head[0] == head[0] + 1:
                    reward += APPROACH_RED_APPLE_PENALTY
                elif i == 3 and new_head[0] == head[0] - 1:
                    reward += APPROACH_RED_APPLE_PENALTY

        self.snake.appendleft(new_head)
        #reward or penalty for eating an apple
        if new_head in self.green_apples:
            reward += GREEN_APPLE_REWARD
            self.green_apples.remove(new_head)
            self.green_apples.append(self._generate_apple())
        elif new_head == self.red_apple:
            reward += RED_APPLE_PENALTY
            self.snake.pop()
            self.red_apple = self._generate_apple()
            if len(self.snake) == 0:
                reward += GAME_OVER_PENALTY
                self.game_over = True
                return self._get_state(), reward, self.game_over
        else:
            self.snake.pop()

        return self._get_state(), reward, self.game_over



