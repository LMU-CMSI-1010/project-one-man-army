import random
from perlin_noise import PerlinNoise

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'north': True, 'east': True, 'south': True, 'west': True}
        self.is_exit = False
        # beginning rooms have all 4 walls and are not exits

class Maze:
    def __init__(self, size=100):
        self.size = size
        # size can be changed in config
        self.noise = PerlinNoise(octaves=1, seed=random.randint(0, 1000))
        # perlin noise generation
        self.rooms = [[Room(x, y) for y in range(size)] for x in range(size)]
        # creates coordinates map for however big the size is (100x100)
        self.generate_maze()
        self.set_exit()

    def generate_maze(self):
        noise = PerlinNoise(octaves=3, seed=random.randint(0, 1000))
        # perlin noise generation
        noise_values = [[noise([x/20, y/20]) for y in range(self.size)] for x in range(self.size)]
        # assign values to each coordinate based on perlin noise
        
        threshold = -0.1
        # sets cutoff value that determines when walls are removed
        for x in range(self.size):
            for y in range(self.size):
                if x > 0:
                # only checks rooms that do not border left wall
                    if noise_values[x][y] > threshold and noise_values[x-1][y] > threshold:
                    # compares noise values of current room [x][y] and room to the west [x-1][y]
                    # if both rooms are greater than threshold
                        self.rooms[x][y].walls['west'] = False
                        # remove west wall of original room
                        self.rooms[x-1][y].walls['east'] = False
                        # remove east wall of room to the west
                        # both walls in both rooms are removed
                if y > 0:
                    if noise_values[x][y] > threshold and noise_values[x][y-1] > threshold:
                        self.rooms[x][y].walls['south'] = False
                        self.rooms[x][y-1].walls['north'] = False
        
        self.ensure_path_exists()

    def ensure_path_exists(self):
        # this is very much unoptimzed lol
        visited = set() # keeps track of visited rooms
        stack = [(0, 0)] # starts from 0,0
        while stack:
        # loops until all rooms are visited
            x, y = stack.pop()
            # updates to next room
            if (x, y) not in visited:
                visited.add((x, y))
                # mark room as visited
                if x > 0 and not self.rooms[x][y].walls['west']:
                    stack.append((x-1, y))
                if x < self.size-1 and not self.rooms[x][y].walls['east']:
                    stack.append((x+1, y))
                if y > 0 and not self.rooms[x][y].walls['south']:
                    stack.append((x, y-1))
                if y < self.size-1 and not self.rooms[x][y].walls['north']:
                    stack.append((x, y+1))
                 # checks each direction, only adds adjacent rooms to stack if no wall between them
        
        if (self.size-1, self.size-1) not in visited:
            # after exploration, check if we reached the far corner
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
             # create path by removing walls until reaching (0,0)

    # probably should have done this differently lol

    def set_exit(self):
        max_noise = float('-inf')
        # get highest value of perlin noise
        main_x = main_y = 0
        for x in range(self.size//2, self.size):
            for y in range(self.size//2, self.size):
                noise_val = self.noise([x/self.size, y/self.size])
                if noise_val > max_noise:
                    max_noise = noise_val
                    main_x = x
                    main_y = y
        self.rooms[main_x][main_y].is_exit = True
        # search top right quadrant for highest noise value, set it as exit
        
        num_extra_exits = random.randint(0, 5)
        extra_exits = set()
        # add any number 0-5 of extra exits
        
        while len(extra_exits) < num_extra_exits:
            x = random.randint(self.size//2, self.size-1)
            y = random.randint(self.size//2, self.size-1)
            if (x, y) != (main_x, main_y):
                extra_exits.add((x, y))
            # select random coords for extra exits
        
        for x, y in extra_exits:
            self.rooms[x][y].is_exit = True
            # set them as exits