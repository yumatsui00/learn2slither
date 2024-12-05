from agent import Agent
from environment import Stage

class GameMaster:
    def __init__(self, agent: Agent, environment: Stage):
        self.agent = agent
        self.environment = environment
