#Stage
CELL_SIZE = 50
GRID_SIZE = 10

#Reward & penalty
MOVE_PENALTY = -5
APPROACH_PENALTY = -1
GREEN_APPLE_REWARD = 300.0
RED_APPLE_PENALTY = -150.0
APPROACH_GREEN_APPLE_REWARD = 0.5
APPROACH_RED_APPLE_PENALTY = -0.5
GAME_OVER_PENALTY = -800.0


#Agent
EPSILON = 0.3
EPSILON_DECAY = 0.995
EPSILON_MIN = 0.01
GAMMA = 0.9
ALPHA = 0.1

#Settings
Default_episodes = 1000
Default_speed = 0
Default_size = 10
Default_model_path = "models/model"

#screen settings
CELL_SIZE = 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)