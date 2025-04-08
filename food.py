import pygame
import numpy as np

class Food:
    def __init__(self, x, y, size=3):
        self.position = np.array([x, y], dtype=float)
        self.size = size
        self.amount = size * size * 5
        self.initial_amount = self.amount

    def take_food(self):
        if self.amount > 0:
            self.amount -= 1
            return True
        return False

    def is_empty(self):
        return self.amount <= 0

    def draw(self, screen, cell_size):
        remaining_ratio = self.amount / self.initial_amount
        current_size = max(1, int(self.size * cell_size * remaining_ratio ** 0.5))
        pos = (int(self.position[0] * cell_size), int(self.position[1] * cell_size))
        pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], current_size, current_size))
