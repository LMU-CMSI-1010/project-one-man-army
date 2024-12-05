import pygame
import config

class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 60)
        self.buttons = {
            'size_up': pygame.Rect(550, 300, 50, 50),
            'size_down': pygame.Rect(200, 300, 50, 50),
            'admin': pygame.Rect(250, 400, 300, 70),
            'back': pygame.Rect(250, 500, 300, 70)
        }
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Draw maze size controls
        size_text = self.font.render(f"Maze Size: {config.SETTINGS['maze_size']}", True, (255, 255, 255))
        self.screen.blit(size_text, (250, 310))
        
        # Draw buttons
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (50, 50, 50), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            
            if name == 'size_up':
                text = '+'
            elif name == 'size_down':
                text = '-'
            elif name == 'admin':
                text = f"Admin: {config.SETTINGS['admin_mode']}"
            else:
                text = name.title()
                
            text_surf = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for name, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    if name == 'size_up':
                        config.SETTINGS['maze_size'] = min(config.SETTINGS['maze_size'] + 10, config.SETTINGS['max_size'])
                    elif name == 'size_down':
                        config.SETTINGS['maze_size'] = max(config.SETTINGS['maze_size'] - 10, config.SETTINGS['min_size'])
                    elif name == 'admin':
                        config.SETTINGS['admin_mode'] = not config.SETTINGS['admin_mode']
                    elif name == 'back':
                        return True
        return False