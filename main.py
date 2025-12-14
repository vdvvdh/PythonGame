#main.py
import pygame
import sys
from image_loader import ImageLoader
from pet import Pet
from ui import UI
from save_system import save_data, load_data
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LIGHT_BLUE

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kitsune - Virtual Pet Game")
        self.clock = pygame.time.Clock()

        #images
        self.image_loader = ImageLoader()
        if not self.image_loader.load_images():
            print("Geen images gevonden, placeholders worden gebruikt.")

        #pet
        stats = load_data()
        self.pet = Pet(stats=stats)

        #ui
        self.ui = UI(self.screen, self.image_loader)

        #auto-save timer
        self.auto_save_timer = 0
        self.auto_save_interval = 30

        #begin console (controls)
        print("\n" + "="*50)
        print("Started Kitsune")
        print("="*50)
        print("\nControls:")
        print("  F - Voeren")
        print("  P - Spelen")
        print("  C - Wassen")
        print("  ESC - Afsluiten en opslaan")
        print("\n" + "="*50 + "\n")

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            # events checken
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.handle_keydown(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)

            # update pet en game
            self.update(dt)

            # teken alles
            self.draw()

            pygame.display.flip()

        self.quit()

    def update(self, dt):
        """update pet stats en auto-save"""
        self.pet.tick()

        #auto-save
        self.auto_save_timer += dt
        if self.auto_save_timer >= self.auto_save_interval:
            save_data(self.pet)
            self.ui.add_notification("Auto save")
            self.auto_save_timer = 0

        #kritieke stats checken
        self.check_critical_stats()

    def check_critical_stats(self):
        """waarschuw bij lage/hoge stats"""
        if self.pet.hunger > 90 and not hasattr(self, '_hunger_warning'):
            self.ui.add_notification("Honger is kritiek!")
            self._hunger_warning = True
        elif self.pet.hunger < 80:
            if hasattr(self, '_hunger_warning'):
                delattr(self, '_hunger_warning')

        if self.pet.energy < 10 and not hasattr(self, '_energy_warning'):
            self.ui.add_notification("Energie is kritiek!")
            self._energy_warning = True
        elif self.pet.energy > 20:
            if hasattr(self, '_energy_warning'):
                delattr(self, '_energy_warning')

        if self.pet.happiness < 20 and not hasattr(self, '_happiness_warning'):
            self.ui.add_notification("Pet is erg verdrietig")
            self._happiness_warning = True
        elif self.pet.happiness > 30:
            if hasattr(self, '_happiness_warning'):
                delattr(self, '_happiness_warning')

    def draw(self):
        """teken alles op het scherm"""
        self.screen.fill(LIGHT_BLUE)

        floor_rect = pygame.Rect(0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150)
        pygame.draw.rect(self.screen, (200, 220, 180), floor_rect)
        pygame.draw.rect(self.screen, (150, 170, 130), floor_rect, 3)

        #pet
        self.draw_pet()

        #ui
        self.ui.draw(self.pet)

        #fps
        if hasattr(self, 'show_fps') and self.show_fps:
            fps_text = self.ui.small_font.render(f"FPS: {int(self.clock.get_fps())}", True, (100, 100, 100))
            self.screen.blit(fps_text, (10, 10))

    def draw_pet(self):
        """Teken pet sprite op basis van mood"""
        mood = self.pet.get_mood()
        pet_image = self.image_loader.get_image(f'pet_{mood}')

        if pet_image:
            pet_scaled = pygame.transform.scale(pet_image, (200, 200))
            pet_rect = pet_scaled.get_rect(center=(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 30))

            #blije kitsune bounce effect
            if self.pet.happiness > 70:
                import math
                bounce = abs(math.sin(pygame.time.get_ticks() / 500)) * 10
                pet_rect.y -= bounce

            self.screen.blit(pet_scaled, pet_rect)
        else:
            #fallback placeholder
            pygame.draw.circle(self.screen, (255, 200, 150), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 50)
            pygame.draw.circle(self.screen, (100, 100, 100), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 50, 3)

    def handle_keydown(self, key):
        """Keyboard input afhandelen"""
        actions = {
            pygame.K_f: 'food',
            pygame.K_p: 'play',
            pygame.K_c: 'clean',
        }

        if key in actions:
            action = actions[key]
            success = self.ui.perform_action(action, self.pet)
            if success:
                button = self.ui.buttons[action]
                self.ui.add_notification(f"✓ {button.label.split('(')[0].strip()}")

    def handle_mouse_click(self, pos):
        """clicks op ui knoppen"""
        pass

    def handle_mouse_motion(self, pos):
        """hover effect"""
        for button in self.ui.buttons.values():
            button.update_hover(pos)

    def quit(self):
        """opslaan en afsluiten"""
        print("\n" + "="*50)
        print("opslaan en afsluiten...")
        save_data(self.pet)
        print("bedankt voor het spelen!")
        print("="*50 + "\n")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"\nFout: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)