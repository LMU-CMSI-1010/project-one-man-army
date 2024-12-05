import random
from perlin_noise import PerlinNoise

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'north': True, 'east': True, 'south': True, 'west': True}
        self.is_exit = False

class Maze:
    def __init__(self, size=100):
        self.size = size
        self.rooms = [[Room(x, y) for y in range(size)] for x in range(size)]
        self.generate_maze()
        self.set_exit()

    def generate_maze(self):
        noise = PerlinNoise(octaves=3, seed=random.randint(0, 1000))
        noise_values = [[noise([x/20, y/20]) for y in range(self.size)] for x in range(self.size)]
        
        threshold = -0.1
        for x in range(self.size):
            for y in range(self.size):
                if x > 0:
                    if noise_values[x][y] > threshold and noise_values[x-1][y] > threshold:
                        self.rooms[x][y].walls['west'] = False
                        self.rooms[x-1][y].walls['east'] = False
                if y > 0:
                    if noise_values[x][y] > threshold and noise_values[x][y-1] > threshold:
                        self.rooms[x][y].walls['south'] = False
                        self.rooms[x][y-1].walls['north'] = False
        
        self.ensure_path_exists()

    def ensure_path_exists(self):
        visited = set()
        stack = [(0, 0)]
        while stack:
            x, y = stack.pop()
            if (x, y) not in visited:
                visited.add((x, y))
                if x > 0 and not self.rooms[x][y].walls['west']:
                    stack.append((x-1, y))
                if x < self.size-1 and not self.rooms[x][y].walls['east']:
                    stack.append((x+1, y))
                if y > 0 and not self.rooms[x][y].walls['south']:
                    stack.append((x, y-1))
                if y < self.size-1 and not self.rooms[x][y].walls['north']:
                    stack.append((x, y+1))
        
        if (self.size-1, self.size-1) not in visited:
            self.create_path_to_exit()

    def create_path_to_exit(self):
        x, y = self.size-1, self.size-1
        while x > 0 or y > 0:
            if x > 0:
                self.rooms[x][y].walls['west'] = False
                self.rooms[x-1][y].walls['east'] = False
                x -= 1
            if y > 0:
                self.rooms[x][y].walls['south'] = False
                self.rooms[x][y-1].walls['north'] = False
                y -= 1

    def set_exit(self):
        self.rooms[self.size-1][self.size-1].is_exit = True