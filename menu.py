import pygame
import sys

class Menu:
    def __init__(self):
        self.WINDOW_SIZE = 800
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Maze Explorer")
        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 60)
        self.buttons = {
            'start': {'rect': pygame.Rect(250, 300, 300, 70), 'color': (50, 50, 50), 'hover': False},
            'settings': {'rect': pygame.Rect(250, 400, 300, 70), 'color': (50, 50, 50), 'hover': False},
            'exit': {'rect': pygame.Rect(250, 500, 300, 70), 'color': (50, 50, 50), 'hover': False}
        }
        self.settings = {'maze_size': 100}
        
    def draw_menu(self):
        # Background
        self.screen.fill((0, 0, 0))
        
        # Title
        title = self.title_font.render('Maze Explorer', True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.WINDOW_SIZE//2, 150))
        self.screen.blit(title, title_rect)
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for text, button in self.buttons.items():
            rect = button['rect']
            # Check hover
            button['hover'] = rect.collidepoint(mouse_pos)
            color = (100, 100, 100) if button['hover'] else button['color']
            
            # Draw button background
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)
            
            # Draw button text
            text_surface = self.button_font.render(text.title(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def handle_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        for button_name, button in self.buttons.items():
                            if button['rect'].collidepoint(event.pos):
                                return button_name
            
            self.draw_menu()
            pygame.display.flip()

def main():
    pygame.init()
    menu = Menu()
    
    while True:
        action = menu.handle_menu()
        if action == 'start':
            import game
            game.run_game()
        elif action == 'settings':
            pass  # Add settings menu later
        elif action == 'exit':
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()