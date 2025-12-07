import os
import pygame

class ImageLoader:
    def __init__(self):
        self.images = {}
        self.image_folder = os.path.join('assets', 'images')

    def load_images(self):
        try:
            self.images['pet_idle'] = pygame.image.load(os.path.join(self.image_folder, 'pet_idle.png')).convert_alpha()
            self.images['pet_happy'] = pygame.image.load(os.path.join(self.image_folder, 'pet_happy.png')).convert_alpha()
            self.images['pet_sad'] = pygame.image.load(os.path.join(self.image_folder, 'pet_sad.png')).convert_alpha()
            self.images['pet_dirty'] = pygame.image.load(os.path.join(self.image_folder, 'pet_dirty.png')).convert_alpha()
            self.images['pet_tired'] = pygame.image.load(os.path.join(self.image_folder, 'pet_tired.png')).convert_alpha()
            self.images['icon_clean'] = pygame.image.load(os.path.join(self.image_folder, 'icon_clean.png')).convert_alpha()
            self.images['icon_food'] = pygame.image.load(os.path.join(self.image_folder, 'icon_food.png')).convert_alpha()
            self.images['icon_play'] = pygame.image.load(os.path.join(self.image_folder, 'icon_play.png')).convert_alpha()
            return True
        except Exception as e:
            print(f"fout bij laden afbeeldingen: {e}")
            return False

    def get_image(self, name):
        return self.images.get(name, None)
