#main.py
import pygame
import sys
from image_loader import ImageLoader
from pet import Pet
from ui import UI
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kitsune - Virtual Pet Game")
        self.clock = pygame.time.Clock()
        
        #images
        self.image_loader = ImageLoader()
        if not self.image_loader.load_images():
            print("geen images geload er worden placeholders gebruikt")
        
        #pet
        self.pet = Pet()
        
        #ui
        self.ui = UI(self.screen, self.image_loader)
        
    def run(self):
        running = True
        while running:
            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
            
            #upd
            self.pet.tick()
            
            # Draw
            self.screen.fill((240, 248, 255))
            
            #draw pet
            pet_image = self.get_pet_image()
            if pet_image:
                pet_rect = pet_image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(pet_image, pet_rect)
            
            #draw UI
            self.ui.draw(self.pet)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def get_pet_image(self):
        """krijg de juiste image gebaseerd op pet's status"""
        if self.pet.happiness <= 30:
            return self.image_loader.get_image('pet_sad')
        elif self.pet.cleanliness <= 40:
            return self.image_loader.get_image('pet_dirty')
        elif self.pet.energy <= 30:
            return self.image_loader.get_image('pet_tired')
        elif self.pet.happiness >= 80:
            return self.image_loader.get_image('pet_happy')
        else:
            return self.image_loader.get_image('pet_idle')
    
    def handle_keydown(self, key):
        """handle keyboard input"""
        if key == pygame.K_f:
            self.pet.feed()
        elif key == pygame.K_p:
            self.pet.play()
        elif key == pygame.K_c:
            self.pet.clean()
    
    def handle_mouse_click(self, pos):
        """handle mouse clicks voor ui buttons"""
        self.ui.handle_click(pos, self.pet)

if __name__ == "__main__":
    game = Game()
    game.run()