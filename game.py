import pygame
from save_system import load_data, save_data
from pet import Pet
from ui import Button, StatBar

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption("Kitsune - Virtual Pet")
        self.clock = pygame.time.Clock()

        #load bestaande pet stats of begin met een nieuwe
        stats = load_data()
        self.pet = Pet(stats=stats)

        #achtergrond en pet images
        self.background = pygame.image.load("assets/images/bg.png")
        self.pet_images = {
            "idle": pygame.image.load("assets/images/pet_idle.png"),
            "happy": pygame.image.load("assets/images/pet_happy.png"),
            "hungry": pygame.image.load("assets/images/pet_sad.png"),
            "dirty": pygame.image.load("assets/images/pet_dirty.png"),
            "tired": pygame.image.load("assets/images/pet_tired.png"),
        }

        #actie knoppen
        self.feed_button = Button(50, 450, pygame.image.load("assets/images/icon_food.png"), 0.4)
        self.play_button = Button(160, 450, pygame.image.load("assets/images/icon_play.png"), 0.4)
        self.clean_button = Button(270, 450, pygame.image.load("assets/images/icon_clean.png"), 0.4)

        #statistiekbalken
        self.hunger_bar = StatBar(550, 80, 250, 20, (120, 50, 50), (255, 100, 100))
        self.energy_bar = StatBar(550, 120, 250, 20, (50, 50, 120), (100, 100, 255))
        self.happiness_bar = StatBar(550, 160, 250, 20, (50, 120, 50), (100, 255, 100))
        self.hygiene_bar = StatBar(550, 200, 250, 20, (120, 120, 50), (255, 255, 100))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_data(self.pet)
                    running = False

                #check of een knop is aangeklikt
                if self.feed_button.is_clicked(event):
                    self.pet.feed()
                if self.play_button.is_clicked(event):
                    self.pet.play()
                if self.clean_button.is_clicked(event):
                    self.pet.clean()

            #update pet stats
            self.pet.tick()

            #alles tekenen
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw(self):
        #achtergrond
        self.screen.blit(self.background, (0, 0))

        #pet images op basis van stemming
        mood = getattr(self.pet, "mood", "idle")
        pet_img = self.pet_images.get(mood, self.pet_images["idle"])
        self.screen.blit(pet_img, (200, 250))

        #butons tekenen
        self.feed_button.draw(self.screen)
        self.play_button.draw(self.screen)
        self.clean_button.draw(self.screen)

        #statistiekbalken tekenen
        self.hunger_bar.draw(self.screen, self.pet.stats["hunger"])
        self.energy_bar.draw(self.screen, self.pet.stats["energy"])
        self.happiness_bar.draw(self.screen, self.pet.stats["happiness"])
        self.hygiene_bar.draw(self.screen, self.pet.stats["hygiene"])
