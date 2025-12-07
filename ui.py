# ui.py (vereenvoudigde versie)
import pygame

class UI:
    def __init__(self, screen, image_loader):
        self.screen = screen
        self.image_loader = image_loader
        self.font = pygame.font.Font(None, 24)
        
        self.buttons = {
            'food': {'rect': pygame.Rect(50, 400, 50, 50), 'action': 'feed'},
            'play': {'rect': pygame.Rect(150, 400, 50, 50), 'action': 'play'},
            'clean': {'rect': pygame.Rect(250, 400, 50, 50), 'action': 'clean'}
        }
    
    def draw(self, pet):
        """draw ui elements"""
        self.draw_bar(50, 50, pet.hunger, (255, 100, 100), "Hunger")
        self.draw_bar(50, 100, pet.happiness, (255, 200, 100), "Happiness")
        self.draw_bar(50, 150, pet.energy, (100, 200, 100), "Energy")
        self.draw_bar(50, 200, pet.cleanliness, (100, 150, 255), "Hygiene")
        
        for button_name, button_info in self.buttons.items():
            rect = button_info['rect']

            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
            
            icon = self.image_loader.get_image(f'icon_{button_name}')
            if icon:
                icon_rect = icon.get_rect(center=rect.center)
                self.screen.blit(icon, icon_rect)
            
            label = self.font.render(button_name.capitalize(), True, (50, 50, 50))
            label_rect = label.get_rect(center=(rect.centerx, rect.bottom + 15))
            self.screen.blit(label, label_rect)
        
        name_text = self.font.render(f"Naam: {pet.name}", True, (50, 50, 50))
        self.screen.blit(name_text, (350, 50))
        
        level_text = self.font.render(f"Level: {pet.level}", True, (50, 50, 50))
        self.screen.blit(level_text, (350, 80))
    
    def draw_bar(self, x, y, value, color, label):
        """draw status bar"""
        bar_width = 200
        bar_height = 20
        
        pygame.draw.rect(self.screen, (220, 220, 220), (x, y, bar_width, bar_height))
        
        fill_width = int((value / 100) * bar_width)
        pygame.draw.rect(self.screen, color, (x, y, fill_width, bar_height))
        
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, bar_width, bar_height), 2)
        
        label_text = self.font.render(f"{label}: {value}%", True, (50, 50, 50))
        self.screen.blit(label_text, (x + bar_width + 10, y))
    
    def handle_click(self, pos, pet):
        """handle button clicks"""
        for button_name, button_info in self.buttons.items():
            if button_info['rect'].collidepoint(pos):
                action = button_info['action']
                if action == 'feed':
                    pet.feed()
                elif action == 'play':
                    pet.play()
                elif action == 'clean':
                    pet.clean()
                print(f"{button_name} button clicked!")

class Button:
    def __init__(self, x, y, image, scale=1.0):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class StatBar:
    def __init__(self, x, y, width, height, bg_color, fill_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fill_color = fill_color
    
    def draw(self, surface, value):
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        
        fill_width = int((value / 100) * self.width)
        pygame.draw.rect(surface, self.fill_color, (self.x, self.y, fill_width, self.height))
        
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)