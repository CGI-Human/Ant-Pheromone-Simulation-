import pygame
import numpy as np
from grid import Grid
from ant import Ant
from food import Food
from obstacle import Obstacle
from pheromone_map import PheromoneMap

# window and grid size 
WIDTH, HEIGHT = 1480, 1000
UI_HEIGHT = 60
SIMULATION_HEIGHT = HEIGHT - UI_HEIGHT
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = SIMULATION_HEIGHT // CELL_SIZE
MAX_ANTS = 100
ANT_SPAWN_RATE = 70
ANTS_PER_SPAWN = 10

# This is for creating the buttons for UI elements 
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    # button properties (do not change)
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)  # Black background
        font = pygame.font.SysFont('Calibri', 24)  # Calibri font
        text = font.render(self.text, True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

# main class
class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
        self.pheromone_map = PheromoneMap(GRID_WIDTH, GRID_HEIGHT)
        self.ants = []
        self.foods = []
        self.obstacles = []
        self.running = True
        self.paused = True
        self.spawn_timer = 0
        self.nest_position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.nest_size = 5
        self.speed_multiplier = 1

        # Set up of the buttons
        button_width = 120
        button_height = 40
        button_margin = 10
        self.buttons = {
            'start': Button(button_margin, 10, button_width, button_height, "Start", (0, 255, 0)),
            'food': Button(button_margin*2 + button_width, 10, button_width, button_height, "Food", (255, 255, 0)),
            'obstacle': Button(button_margin*3 + button_width*2, 10, button_width, button_height, "Obstacle", (128, 128, 128)),
            'speed': Button(button_margin*4 + button_width*3, 10, button_width, button_height, "Speed: 1x", (0, 0, 255))
        }
        self.active_tool = None

    # This is the main loop that runs the simulation
    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused:
                for _ in range(self.speed_multiplier):
                    self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    # Handling user inputs like mouse clicks and checking position to place the objects 
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    # What to do when the user clicks somewhere
    def handle_mouse_click(self, pos):
        if pos[1] < UI_HEIGHT:
            for button_name, button in self.buttons.items():
                if button.rect.collidepoint(pos):
                    if button_name == 'start':
                        self.paused = not self.paused
                        self.buttons['start'].text = "Pause" if not self.paused else "Start"
                    elif button_name == 'speed':
                        self.speed_multiplier = (self.speed_multiplier % 3) + 1
                        self.buttons['speed'].text = f"Speed: {self.speed_multiplier}x"
                    else:
                        self.active_tool = button_name
                    return
        else:
            if self.active_tool:
                grid_x = pos[0] // CELL_SIZE
                grid_y = (pos[1] - UI_HEIGHT) // CELL_SIZE
                if self.active_tool == 'obstacle':
                    self.obstacles.append(Obstacle(grid_x, grid_y, 3))
                elif self.active_tool == 'food':
                    new_food = Food(grid_x, grid_y, 3)
                    self.foods.append(new_food)
                    print(f"Food placed at {new_food.position}")

    # Update the state of the simulation
    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer >= ANT_SPAWN_RATE and len(self.ants) < MAX_ANTS:
            self.spawn_ants()
            self.spawn_timer = 0

        for ant in self.ants:
            ant.move(self.grid, self.pheromone_map, self.foods, self.obstacles)

        self.pheromone_map.update()

        for food in self.foods[:]:
            if food.is_empty():
                print(f"Food at {food.position} is depleted")
                self.foods.remove(food)

    # Creating new ants at the ant nest
    def spawn_ants(self):
        x, y = self.nest_position
        for _ in range(ANTS_PER_SPAWN):
            if len(self.ants) < MAX_ANTS:
                new_ant = Ant(x, y, self.nest_position, GRID_WIDTH, GRID_HEIGHT)
                self.ants.append(new_ant)
        print(f"Spawned {ANTS_PER_SPAWN} ants. Total ants: {len(self.ants)}")

    # Draw everything on the screen
    def draw(self):
        self.screen.fill((255, 255, 255))

        simulation_surface = pygame.Surface((WIDTH, SIMULATION_HEIGHT))
        simulation_surface.fill((255, 255, 255))

        self.pheromone_map.draw(simulation_surface, CELL_SIZE)

        # Draw the nest
        nest_color = (139, 69, 19)
        nest_points = [
            (self.nest_position[0] * CELL_SIZE, self.nest_position[1] * CELL_SIZE),
            ((self.nest_position[0] + self.nest_size) * CELL_SIZE, self.nest_position[1] * CELL_SIZE),
            ((self.nest_position[0] + self.nest_size // 2) * CELL_SIZE,
             (self.nest_position[1] - self.nest_size) * CELL_SIZE)
        ]
        pygame.draw.polygon(simulation_surface, nest_color, nest_points)

        # Draw food, obstacles, and ants
        for food in self.foods:
            food.draw(simulation_surface, CELL_SIZE)
        for obstacle in self.obstacles:
            obstacle.draw(simulation_surface, CELL_SIZE)
        for ant in self.ants:
            ant.draw(simulation_surface, CELL_SIZE)

        self.screen.blit(simulation_surface, (0, UI_HEIGHT))

        # Draw the UI
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, WIDTH, UI_HEIGHT))
        for button in self.buttons.values():
            button.draw(self.screen)

        pygame.display.flip()

# Start the simulation
if __name__ == "__main__":
    sim = Simulation()
    sim.run()
