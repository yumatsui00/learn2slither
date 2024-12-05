import numpy as np

class Stage:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size))

