import pygame

class Button:
    def __init__(self, x, y, image, scale=1.0, label=""):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hovered = False
        self.label = label

    def draw(self, surface):
        outline_color = (255, 200, 50) if self.hovered else (100, 100, 100)
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, outline_color, self.rect, 2)
        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

class StatBar:
    def __init__(self, x, y, width, height, bg_color, fill_color, label=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.label = label
        self.font = pygame.font.Font(None, 20)

    def draw(self, surface, value):
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        fill_width = int((value / 100) * self.width)
        pygame.draw.rect(surface, self.fill_color, (self.x, self.y, fill_width, self.height))
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        if self.label:
            text = self.font.render(f"{self.label}: {int(value)}%", True, (0, 0, 0))
            surface.blit(text, (self.x + self.width + 10, self.y))

class UI:
    def __init__(self, screen, image_loader):
        self.screen = screen
        self.image_loader = image_loader

        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        self.buttons = {
            'food': Button(50, 400, self.image_loader.get_image('icon_food'), 0.7, label="Voeren"),
            'play': Button(150, 400, self.image_loader.get_image('icon_play'), 0.7, label="Spelen"),
            'clean': Button(250, 400, self.image_loader.get_image('icon_clean'), 0.7, label="Wassen")
        }

        self.hunger_bar = StatBar(50, 50, 200, 20, (220, 220, 220), (255, 100, 100), "Hunger")
        self.happiness_bar = StatBar(50, 80, 200, 20, (220, 220, 220), (255, 200, 100), "Happiness")
        self.energy_bar = StatBar(50, 110, 200, 20, (220, 220, 220), (100, 255, 100), "Energy")
        self.cleanliness_bar = StatBar(50, 140, 200, 20, (220, 220, 220), (100, 150, 255), "Hygiene")

        self.notifications = []

    def draw(self, pet):
        self.hunger_bar.draw(self.screen, pet.hunger)
        self.happiness_bar.draw(self.screen, pet.happiness)
        self.energy_bar.draw(self.screen, pet.energy)
        self.cleanliness_bar.draw(self.screen, pet.cleanliness)

        for button in self.buttons.values():
            button.draw(self.screen)

        name_text = self.font.render(f"Naam: {pet.name}", True, (50, 50, 50))
        self.screen.blit(name_text, (350, 50))

        level_text = self.font.render(f"Level: {pet.level}", True, (50, 50, 50))
        self.screen.blit(level_text, (350, 80))

        for i, note in enumerate(self.notifications[-5:]):
            text = self.small_font.render(note, True, (0, 0, 0))
            self.screen.blit(text, (50, 500 + i*20))

    def handle_click(self, pos, pet):
        for name, button in self.buttons.items():
            if button.rect.collidepoint(pos):
                if name == "food":
                    pet.feed()
                elif name == "play":
                    pet.play()
                elif name == "clean":
                    pet.clean()
                self.add_notification(f"{button.label} uitgevoerd!")

    def perform_action(self, action, pet):
        """Called bij keypress F, P, C"""
        if action == "food":
            success = pet.feed()
        elif action == "play":
            success = pet.play()
        elif action == "clean":
            success = pet.clean()
        else:
            success = False
        return success

    def add_notification(self, text):
        self.notifications.append(text)