from parser import parse_args
from agent import Agent
from environment import Stage
from interpretr import GameMaster
import numpy as np


def main():
    args = parse_args()
    # print(args)
    if args.visualize:
        print("Visualizing")
    agent = Agent(not args.no_learning)
    stage = Stage(args.size)

    if args.load:
        # agent.load(args.load)
        print(f"Loading model from {args.load}")
    master = GameMaster(agent, stage)

    episode = 0
    running = True
    while running and episode < args.episodes:
        master.play_episode(episode)
        episode += 






if __name__ == "__main__":
    main()