import pygame
from perlin_noise import PerlinNoise
import sys
import random

WINDOW_SIZE = 800
ROOM_SIZE = 8  # Smaller room size for 100x100 maze
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Room:
   def __init__(self, x, y):
       self.x = x
       self.y = y
       self.walls = {'north': True, 'east': True, 'south': True, 'west': True}
       self.is_exit = False
       self.discovered = False
       self.discovered_walls = {'north': False, 'east': False, 'south': False, 'west': False}

class Maze:
   def __init__(self, size=100):
       self.size = size
       self.current_x = 0
       self.current_y = 0
       self.rooms = [[Room(x, y) for y in range(size)] for x in range(size)]
       self.generate_maze()
       self.set_exit()
       self.discover_current_room()
   
   def discover_current_room(self):
       current = self.rooms[self.current_x][self.current_y]
       current.discovered = True
       for direction in ['north', 'east', 'south', 'west']:
           current.discovered_walls[direction] = True

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
   
   def can_move(self, direction):
       room = self.rooms[self.current_x][self.current_y]
       return not room.walls[direction]
   
   def move(self, key):
       moves = {
           pygame.K_UP: ('north', 0, 1),
           pygame.K_RIGHT: ('east', 1, 0),
           pygame.K_DOWN: ('south', 0, -1),
           pygame.K_LEFT: ('west', -1, 0)
       }
       
       if key in moves:
           direction, dx, dy = moves[key]
           if self.can_move(direction):
               new_x = self.current_x + dx
               new_y = self.current_y + dy
               if 0 <= new_x < self.size and 0 <= new_y < self.size:
                   self.current_x = new_x
                   self.current_y = new_y
                   self.discover_current_room()
                   return True
       return False

def draw_maze(screen, maze):
   center_x = WINDOW_SIZE // 2
   center_y = WINDOW_SIZE // 2
   offset_x = center_x - maze.current_x * ROOM_SIZE
   offset_y = center_y + maze.current_y * ROOM_SIZE
   
   for x in range(maze.size):
       for y in range(maze.size):
           room = maze.rooms[x][y]
           if room.discovered:
               room_x = x * ROOM_SIZE + offset_x
               room_y = -y * ROOM_SIZE + offset_y
               
               if room.walls['north']:
                   pygame.draw.line(screen, WHITE, 
                       (room_x, room_y), 
                       (room_x + ROOM_SIZE, room_y), 1)
               if room.walls['south']:
                   pygame.draw.line(screen, WHITE, 
                       (room_x, room_y + ROOM_SIZE), 
                       (room_x + ROOM_SIZE, room_y + ROOM_SIZE), 1)
               if room.walls['west']:
                   pygame.draw.line(screen, WHITE, 
                       (room_x, room_y), 
                       (room_x, room_y + ROOM_SIZE), 1)
               if room.walls['east']:
                   pygame.draw.line(screen, WHITE, 
                       (room_x + ROOM_SIZE, room_y), 
                       (room_x + ROOM_SIZE, room_y + ROOM_SIZE), 1)
               
               if room.is_exit:
                   pygame.draw.rect(screen, RED, 
                       (room_x + 2, room_y + 2, 
                        ROOM_SIZE - 4, ROOM_SIZE - 4))
   
   # Draw player
   player_x = center_x - ROOM_SIZE//4
   player_y = center_y - ROOM_SIZE//4
   pygame.draw.rect(screen, WHITE, 
       (player_x, player_y, ROOM_SIZE//2, ROOM_SIZE//2))

   # Draw coordinates
   font = pygame.font.Font(None, 36)
   pos_text = font.render(f"Position: ({maze.current_x}, {maze.current_y})", True, WHITE)
   screen.blit(pos_text, (10, 10))

def main():
   pygame.init()
   screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
   pygame.display.set_caption("Maze Explorer")
   clock = pygame.time.Clock()
   
   maze = Maze()
   
   running = True
   while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.KEYDOWN:
               if event.key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]:
                   maze.move(event.key)
                   if maze.rooms[maze.current_x][maze.current_y].is_exit:
                       print("Congratulations! You found the exit!")
                       running = False
       
       screen.fill(BLACK)
       draw_maze(screen, maze)
       pygame.display.flip()
       clock.tick(60)
   
   pygame.quit()
   sys.exit()

if __name__ == "__main__":
   main()