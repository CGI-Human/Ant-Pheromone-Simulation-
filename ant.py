import numpy as np
import pygame
from pheromone_map import PheromoneType

class Ant:
    # States an ant can be in
    EXPLORING = 0
    RETURNING = 1

    def __init__(self, x, y, nest_position, grid_width, grid_height):
        # ant's initial properties
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.random.rand(2) - 0.5
        self.velocity /= np.linalg.norm(self.velocity)
        self.nest_position = nest_position
        self.state = self.EXPLORING
        self.has_food = False
        self.speed = 1.0
        self.sensor_offset_distance = 3
        self.sensor_angle_offset = np.pi / 6
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.max_turn_angle = np.pi / 4
        self.target_food = None
        self.stuck_time = 0
        self.random_movement_chance = 0.3

    def move(self, grid, pheromone_map, foods, obstacles):
        # Main function for ant movement and behavior
        if self.state == self.EXPLORING:
            self.target_food = self.find_closest_food(foods)
            if self.target_food is not None:
                self.collect_food()

        # ants Decide randomly whether to move randomly or follow pheromones
        if self.state == self.EXPLORING and np.random.random() < self.random_movement_chance:
            desired_direction = self.get_random_direction()
        else:
            desired_direction = self.get_desired_direction(pheromone_map)

        # this is for calculating new direction and updating the velocity
        current_angle = np.arctan2(self.velocity[1], self.velocity[0])
        desired_angle = np.arctan2(desired_direction[1], desired_direction[0])
        angle_diff = (desired_angle - current_angle + np.pi) % (2 * np.pi) - np.pi
        limited_angle = current_angle + np.clip(angle_diff, -self.max_turn_angle, self.max_turn_angle)

        self.velocity = np.array([np.cos(limited_angle), np.sin(limited_angle)])
        self.velocity *= self.speed

        # Try to move to the new position
        new_position = self.position + self.velocity

        if self.is_valid_position(new_position, grid, obstacles):
            self.position = new_position
            self.stuck_time = 0
        else:
            # If stuck, get unstuck.
            self.stuck_time += 1
            if self.stuck_time > 10:
                self.velocity = np.random.rand(2) - 0.5
                self.velocity /= np.linalg.norm(self.velocity)
                self.stuck_time = 0

        # Leave pheromone trail
        pheromone_type = PheromoneType.SEARCH if self.state == self.EXPLORING else PheromoneType.RETURN
        pheromone_map.deposit_pheromone(self.position, pheromone_type)

        # Check if returned to nest with food
        if self.state == self.RETURNING and np.linalg.norm(self.position - self.nest_position) < 1:
            self.drop_food()

    def get_random_direction(self):
        # Generate a random direction
        random_angle = np.random.uniform(0, 2 * np.pi)
        return np.array([np.cos(random_angle), np.sin(random_angle)])

    def collect_food(self):
        # Collect food if found
        if self.target_food and self.target_food.take_food():
            self.has_food = True
            self.state = self.RETURNING
            self.velocity = (self.nest_position - self.position)
            self.velocity /= np.linalg.norm(self.velocity)

    def drop_food(self):
        # Drop food at the nest
        self.has_food = False
        self.state = self.EXPLORING
        self.target_food = None
        self.velocity = np.random.rand(2) - 0.5
        self.velocity /= np.linalg.norm(self.velocity)

    def find_closest_food(self, foods):
        # Look for the nearest food source
        closest_food = None
        closest_distance = float('inf')
        for food in foods:
            distance = np.linalg.norm(food.position - self.position)
            if distance < closest_distance and distance < self.sensor_offset_distance:
                closest_food = food
                closest_distance = distance
        return closest_food

    def get_desired_direction(self, pheromone_map):
        # Decide which direction to move based on state
        if self.state == self.EXPLORING:
            return self.sense_pheromones(pheromone_map, PheromoneType.RETURN)
        elif self.state == self.RETURNING:
            return (self.nest_position - self.position) / np.linalg.norm(self.nest_position - self.position)

    def sense_pheromones(self, pheromone_map, pheromone_type):
        # Check pheromones in three directions (left, center, right)
        left_sensor = self.position + self.sensor_offset_distance * self.get_sensor_vector(-self.sensor_angle_offset)
        center_sensor = self.position + self.sensor_offset_distance * self.get_sensor_vector(0)
        right_sensor = self.position + self.sensor_offset_distance * self.get_sensor_vector(self.sensor_angle_offset)

        left_strength = pheromone_map.get_pheromone_strength(left_sensor, pheromone_type)
        center_strength = pheromone_map.get_pheromone_strength(center_sensor, pheromone_type)
        right_strength = pheromone_map.get_pheromone_strength(right_sensor, pheromone_type)

        # Choose direction based on pheromone strength
        if center_strength >= max(left_strength, right_strength):
            return self.velocity
        elif left_strength > right_strength:
            return self.get_sensor_vector(-self.sensor_angle_offset)
        else:
            return self.get_sensor_vector(self.sensor_angle_offset)

    def get_sensor_vector(self, angle_offset):
        # Calculate the direction vector for a sensor
        angle = np.arctan2(self.velocity[1], self.velocity[0]) + angle_offset
        return np.array([np.cos(angle), np.sin(angle)])

    def is_valid_position(self, position, grid, obstacles):
        # Check if a position is valid (within grid and not in an obstacle)
        if position[0] < 0 or position[0] >= self.grid_width or position[1] < 0 or position[1] >= self.grid_height:
            return False

        for obstacle in obstacles:
            if obstacle.is_solid(position):
                return False

        return True

    def draw(self, screen, cell_size):
        # Draw the ant on the screen
        x, y = int(self.position[0] * cell_size), int(self.position[1] * cell_size)
        color = (255, 0, 0) if self.has_food else (0, 0, 0)
        pygame.draw.circle(screen, color, (x, y), cell_size // 3)
