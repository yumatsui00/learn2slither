from utils.parser import parse_args
from modules.agent import Agent
from modules.environment import Stage
import numpy as np
import time

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


def main():
    args = parse_args()
    # print(args)
    if args.visualize:
        print("Visualizing")
    snake = Agent(not args.no_learning)
    stage = Stage(args.size)

    if args.load:
        # agent.load(args.load)
        print(f"Loading model from {args.load}")

    episode = 0
    running = True
    while running and episode < args.episodes:
        snake_vision = snake.look_around(stage, print_vision=args.visualize)
        action = snake.get_action(snake_vision)
        #action = 2
        next_state, reward, game_over = stage.step(snake, action, snake_vision)
        # 次回個々から
        #snake.learn(stage, next_state, reward, action)

        if game_over:
            print(f"Episode {episode} finished with length {len(stage.snake)}")
            episode += 1
            stage.reset()

        if not args.step_mode:
            time.sleep(args.speed)
    if args.save:
        print(f"Saving model to {args.save}")
        #snake.save(args.save)


if __name__ == "__main__":
    main()