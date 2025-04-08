import numpy as np
import pygame

class PheromoneType:
    # Different types of pheromones
    SEARCH = 0
    RETURN = 1

class PheromoneMap:
    def __init__(self, width, height):
        # Set up the pheromone map
        self.width = width
        self.height = height
        self.pheromones = {
            PheromoneType.SEARCH: np.zeros((height, width)),
            PheromoneType.RETURN: np.zeros((height, width))
        }
        self.evaporation_rate = 0.995
        self.diffusion_rate = 0.1

    def deposit_pheromone(self, position, pheromone_type, amount=1.0):
        # Add pheromones to a specific location
        x, y = int(position[0]), int(position[1])
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pheromones[pheromone_type][y, x] += amount

    def update(self):
        # Update pheromone levels (evaporation and diffusion)
        for ptype in self.pheromones:
            self.pheromones[ptype] *= self.evaporation_rate
            self.pheromones[ptype] = self.diffuse(self.pheromones[ptype])

    def diffuse(self, pheromone):
        # Spread pheromones to nearby cells
        return pheromone * (1 - self.diffusion_rate) + \
               np.roll(pheromone, 1, axis=0) * self.diffusion_rate / 8 + \
               np.roll(pheromone, -1, axis=0) * self.diffusion_rate / 8 + \
               np.roll(pheromone, 1, axis=1) * self.diffusion_rate / 8 + \
               np.roll(pheromone, -1, axis=1) * self.diffusion_rate / 8

    def get_pheromone_strength(self, position, pheromone_type):
        # Get the strength of pheromones at a specific location
        x, y = int(position[0]), int(position[1])
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pheromones[pheromone_type][y, x]
        return 0.0

    def draw(self, screen, cell_size):
        # Visualizing the pheromone trails on the screen
        search_surface = pygame.Surface((self.width * cell_size, self.height * cell_size), pygame.SRCALPHA)
        return_surface = pygame.Surface((self.width * cell_size, self.height * cell_size), pygame.SRCALPHA)

        for y in range(self.height):
            for x in range(self.width):
                search_strength = min(self.pheromones[PheromoneType.SEARCH][y, x] * 255, 255)
                return_strength = min(self.pheromones[PheromoneType.RETURN][y, x] * 255, 255)

                if search_strength > 0:
                    pygame.draw.rect(search_surface, (0, 255, 0, int(search_strength)),
                                     (x * cell_size, y * cell_size, cell_size, cell_size))
                if return_strength > 0:
                    pygame.draw.rect(return_surface, (255, 0, 0, int(return_strength)),
                                     (x * cell_size, y * cell_size, cell_size, cell_size))

        screen.blit(search_surface, (0, 0))
        screen.blit(return_surface, (0, 0))
