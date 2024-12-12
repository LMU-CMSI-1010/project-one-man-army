'''
Maze Generator Game Engine
By Tim O'Hara
'''
import pygame
import sys
from maze_generator import Maze 
import config
import menu

WINDOW_SIZE = 800
ROOM_SIZE = 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
RED = (255, 0, 0)

class Player:
    def __init__(self, maze):
        self.maze = maze
        self.x = 0
        self.y = 0
        # starting coordinates
        self.discovered_rooms = set()
        self.discovered_exits = set()
        # tuples for rooms and exits
        if config.SETTINGS['admin_mode']:
            self.discover_all_rooms()
            # admin mode to test maze generation
        else:
            self.discover_room()
            # only discover starting room

    def discover_all_rooms(self):
        for x in range(self.maze.size):
            for y in range(self.maze.size):
                self.discovered_rooms.add((x, y))
                if self.maze.rooms[x][y].is_exit:
                    self.discovered_exits.add((x, y))
                    # reveals all rooms and exits

    def discover_room(self):
        self.discovered_rooms.add((self.x, self.y))
        if self.maze.rooms[self.x][self.y].is_exit:
            self.discovered_exits.add((self.x, self.y))
            # called whenever player enters new room, marks current room as discovered and reveals it

    def move(self, key):
        moves = {
            pygame.K_UP: ('north', 0, 1),
            pygame.K_RIGHT: ('east', 1, 0),
            pygame.K_DOWN: ('south', 0, -1),
            pygame.K_LEFT: ('west', -1, 0)
        }
        #controls
        if key in moves:
            direction, dx, dy = moves[key]
            if not self.maze.rooms[self.x][self.y].walls[direction]:
                new_x = self.x + dx
                new_y = self.y + dy
                # only updates coordinates if there is not a wall in the way
                if 0 <= new_x < self.maze.size and 0 <= new_y < self.maze.size:
                    self.x = new_x
                    self.y = new_y
                    self.discover_room()
                    return True
                    # makes sure you don't move outside maze walls
        return False

def draw_game(screen, maze, player):
    # renders game state to screen
    screen.fill(BLACK)
    
    center_x = WINDOW_SIZE // 2
    center_y = WINDOW_SIZE // 2
    offset_x = center_x - player.x * ROOM_SIZE
    offset_y = center_y + player.y * ROOM_SIZE
    # calculate center of screen and offset for player-centered view
    
    for (x, y) in player.discovered_rooms:
        room = maze.rooms[x][y]
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
        # draws white walls for rooms
        
        if (x, y) in player.discovered_exits:
            pygame.draw.rect(screen, RED, 
                (room_x + 2, room_y + 2, 
                 ROOM_SIZE - 4, ROOM_SIZE - 4))
        # exits are red
    
    player_x = center_x - ROOM_SIZE//4
    player_y = center_y - ROOM_SIZE//4
    pygame.draw.rect(screen, WHITE, 
        (player_x, player_y, ROOM_SIZE//2, ROOM_SIZE//2))
    
    # player is white cube

    font = pygame.font.Font(None, 36)
    pos_text = font.render(f"Position: ({player.x}, {player.y})", True, WHITE)
    screen.blit(pos_text, (10, 10))

    #player coordinates in top left

def run_game():
   # game loop
   screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
   clock = pygame.time.Clock()
   maze = Maze(config.SETTINGS['maze_size'])
   player = Player(maze)
   
   running = True
   while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               return
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   return
               if event.key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]:
                   player.move(event.key)
                   if maze.rooms[player.x][player.y].is_exit:
                       print("Congratulations!")
                       # end game when player reaches exit
                       return
       
       draw_game(screen, maze, player)
       pygame.display.flip()
       clock.tick(60)
       # 60 fps!

def main():
   menu.main()
   # main menu

if __name__ == "__main__":
   main()