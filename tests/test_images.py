#tests
import pygame
import sys
import os

#path to the image
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(BASE_DIR, "assets/images/pet_idle.png")

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

#laad een test image
try:
    print(f"probeer image te laden van: {IMAGE_PATH}")
    test_image = pygame.image.load(IMAGE_PATH).convert_alpha()
    print("image succesvol geladen!")
except Exception as e:
    print(f"image niet geladen fout: {e}")
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))
    screen.blit(test_image, (100, 100))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()