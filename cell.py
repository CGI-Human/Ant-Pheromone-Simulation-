import pygame

class Cell:
    def __init__(self, grid_x, grid_y, cell_size):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cell_size = cell_size
        self.color = (255, 255, 255)  # Default color for a cell

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.grid_x * self.cell_size, self.grid_y * self.cell_size, self.cell_size, self.cell_size), 1)
