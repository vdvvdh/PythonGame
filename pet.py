#pet.py
import random
from datetime import datetime

class Pet:
    def __init__(self, name="Kitsune"):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.cleanliness = 50
        self.age = 0
        self.level = 1
        self.last_checked = datetime.now()

    def tick(self):
        """werk stats van de pet bij naarmate de tijd verstrijkt"""
        now = datetime.now()
        minutes_passed = (now - self.last_checked).seconds / 60

        if minutes_passed >= 1:
            #honger neemt toe energie daalt hygiene gaat omlaag
            self.hunger = min(100, self.hunger + random.randint(1, 3))
            self.energy = max(0, self.energy - random.randint(1, 2))
            self.cleanliness = max(0, self.cleanliness - random.randint(0, 1))

            #happiness beinvloed door honger en energie
            if self.hunger > 80 or self.energy < 20:
                self.happiness = max(0, self.happiness - 1)

            self.last_checked = now

    def feed(self):
        """geef de pet eten"""
        self.hunger = max(0, self.hunger - 20)
        self.happiness = min(100, self.happiness + 5)

    def play(self):
        """speel met de pet"""
        if self.energy > 10:
            self.energy = max(0, self.energy - 10)
            self.happiness = min(100, self.happiness + 15)
            self.hunger = min(100, self.hunger + 5)

    def clean(self):
        """maak de pet schoon"""
        self.cleanliness = min(100, self.cleanliness + 30)
        self.happiness = min(100, self.happiness + 5)

    def get_stats(self):
        """geef een overzicht van de huidige stats van de pet"""
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "cleanliness": self.cleanliness,
            "age": self.age,
            "level": self.level
        }