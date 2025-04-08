import pygame
import numpy as np

class Obstacle:
    def __init__(self, x, y, size):
        self.position = np.array([x, y], dtype=float)
        self.size = size

    def is_solid(self, position):
        return (self.position[0] <= position[0] < self.position[0] + self.size and
                self.position[1] <= position[1] < self.position[1] + self.size)

    def draw(self, screen, cell_size):
        pos = (int(self.position[0] * cell_size), int(self.position[1] * cell_size))
        size = (int(self.size * cell_size), int(self.size * cell_size))
        pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(pos, size))
