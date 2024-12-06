import argparse
from config import Default_episodes, Default_speed, Default_size, Default_model_path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--visualize", action="store_true")
    parser.add_argument("--terminal_visualize", action="store_true")
    parser.add_argument("--episodes", type=int, default=Default_episodes)
    parser.add_argument("--speed", type=float, default=Default_speed)
    parser.add_argument("--step_mode", action="store_true")
    parser.add_argument("--no_learning", action="store_true")
    parser.add_argument("--load", type=str, default=None, help="path to load model from")
    parser.add_argument("--save", type=str, default=Default_model_path, help="path to save model to")
    parser.add_argument("--size", type=int, default=Default_size)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(args)
