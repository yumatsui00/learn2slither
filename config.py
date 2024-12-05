#Stage
CELL_SIZE = 50
GRID_SIZE = 10

#Reward & penalty
MOVE_PENALTY = -1
APPROACH_PENALTY = -2
GREEN_APPLE_REWARD = 15.0
RED_APPLE_PENALTY = -15.0
APPROACH_GREEN_APPLE_REWARD = 0.5
APPROACH_RED_APPLE_PENALTY = -0.5
GAME_OVER_PENALTY = -500.0


#Agent
EPSILON = 0.1
EPSILON_DECAY = 0.995
EPSILON_MIN = 0.01
GAMMA = 0.9
ALPHA = 0.1

#Settings
Default_episodes = 1000
Default_speed = 0.1
Default_size = 10
Default_model_path = "models/model"