import numpy as np

class GridCell:
    def __init__(self):
        self.pheromones = {}
        self.ants = []


class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width // cell_size
        self.height = height // cell_size
        self.cell_size = cell_size
        self.cells = np.array([[GridCell() for _ in range(self.height)] for _ in range(self.width)])

    def get_cell_coords(self, pos):
        x_cell = int(pos[0] // self.cell_size)
        y_cell = int(pos[1] // self.cell_size)
        return (x_cell, y_cell)

    def get_cell(self, pos):
        coords = self.get_cell_coords(pos)
        if 0 <= coords[0] < self.width and 0 <= coords[1] < self.height:
            return self.cells[coords[0]][coords[1]]
        return None

    def add_ant(self, ant):
        cell = self.get_cell(ant.position)
        if cell:
            cell.ants.append(ant)

    def remove_ant(self, ant):
        cell = self.get_cell(ant.position)
        if cell and ant in cell.ants:
            cell.ants.remove(ant)

    def add_pheromone(self, pos, colony_id, intensity, pheromone_type="food"):
        cell = self.get_cell(pos)
        if cell:
            if pheromone_type not in cell.pheromones:
                cell.pheromones[pheromone_type] = {}
            if colony_id not in cell.pheromones[pheromone_type]:
                cell.pheromones[pheromone_type][colony_id] = 0
            cell.pheromones[pheromone_type][colony_id] += intensity

    def get_pheromones(self, pos, pheromone_type="food"):
        cell = self.get_cell(pos)
        if cell and pheromone_type in cell.pheromones:
            return cell.pheromones[pheromone_type]
        return {}

    def decay_pheromones(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]
                for pheromone_type in cell.pheromones:
                    for colony_id in cell.pheromones[pheromone_type]:
                        cell.pheromones[pheromone_type][colony_id] *= 0.995  # Decay rate

    def diffuse_pheromones(self):
        new_pheromones = np.array([[GridCell() for _ in range(self.height)] for _ in range(self.width)])

        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]
                for pheromone_type in cell.pheromones:
                    for colony_id, intensity in cell.pheromones[pheromone_type].items():
                        neighbors = [
                            (x + dx, y + dy)
                            for dx in [-1, 0, 1]
                            for dy in [-1, 0, 1]
                            if 0 <= x + dx < self.width and 0 <= y + dy < self.height
                        ]
                        for nx, ny in neighbors:
                            if pheromone_type not in new_pheromones[nx][ny].pheromones:
                                new_pheromones[nx][ny].pheromones[pheromone_type] = {}
