#pet.py
import random
from datetime import datetime

class Pet:
    def __init__(self, stats=None, name="Kitsune"):
        """maak een pet aan met defaults of gegeven stats"""
        if stats is None:
            self.name = name
            self.hunger = 50
            self.happiness = 50
            self.energy = 50
            self.cleanliness = 50
            self.age = 0
            self.level = 1
            self.experience = 0
        else:
            self.name = stats.get("name", name)
            self.hunger = stats.get("hunger", 50)
            self.happiness = stats.get("happiness", 50)
            self.energy = stats.get("energy", 50)
            self.cleanliness = stats.get("cleanliness", 50)
            self.age = stats.get("age", 0)
            self.level = stats.get("level", 1)
            self.experience = stats.get("experience", 0)

        self.last_checked = datetime.now()
        self.age_timer = 0

    def tick(self):
        """Update stats over tijd"""
        now = datetime.now()
        seconds_passed = (now - self.last_checked).total_seconds()

        if seconds_passed >= 1:
            #growth
            self.age_timer += seconds_passed
            if self.age_timer >= 60:
                self.age += 1
                self.age_timer = 0

            #stat decay
            decay_factor = seconds_passed / 60
            self.hunger = min(100, self.hunger + 2 * decay_factor)
            self.energy = max(0, self.energy - 1 * decay_factor)
            self.cleanliness = max(0, self.cleanliness - 1 * decay_factor)

            #geluk beinvloed door andere stats
            if self.hunger > 80:
                self.happiness = max(0, self.happiness - 0.5)
            if self.energy < 20:
                self.happiness = max(0, self.happiness - 0.5)
            if self.cleanliness < 30:
                self.happiness = max(0, self.happiness - 0.3)

            self.happiness = max(0, self.happiness - 0.5 * decay_factor)

            self.last_checked = now

    def feed(self):
        """feed de pet"""
        if self.hunger > 10:
            self.hunger = max(0, self.hunger - 20)
            self.happiness = min(100, self.happiness + 5)
            self._gain_experience(10)
            return True
        return False

    def play(self):
        """play met de pet"""
        if self.energy > 10:
            self.energy = max(0, self.energy - 10)
            self.happiness = min(100, self.happiness + 15)
            self.hunger = min(100, self.hunger + 5)
            self._gain_experience(15)
            return True
        return False

    def clean(self):
        """was pet"""
        if self.cleanliness < 80:
            self.cleanliness = min(100, self.cleanliness + 30)
            self.happiness = min(100, self.happiness + 5)
            self._gain_experience(10)
            return True
        return False

    def sleep(self):
        """laat de pet slapen"""
        if self.energy < 100:
            self.energy = min(100, self.energy + 50)
            self.hunger = min(100, self.hunger + 10)
            self._gain_experience(5)
            return True
        return False

    def _gain_experience(self, amount):
        """ervaring en level up"""
        self.experience += amount
        while self.experience >= 100:
            self.level += 1
            self.experience -= 100

    def get_mood(self):
        """mood"""
        if self.happiness <= 30:
            return "sad"
        elif self.cleanliness <= 40:
            return "dirty"
        elif self.energy <= 30:
            return "tired"
        elif self.happiness >= 80:
            return "happy"
        else:
            return "idle"

    def get_status(self):
        """toont status tekst"""
        if self.hunger > 80:
            return "Ik heb honger!"
        elif self.energy < 20:
            return "Ik ben moe.."
        elif self.cleanliness < 30:
            return "Ik ben vies"
        elif self.happiness < 30:
            return "Ik ben verdrietig"
        elif self.happiness > 80:
            return "Ik ben blij!"
        else:
            return "Alles goed!"

    def get_stats(self):
        """stats teruggeven"""
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "cleanliness": self.cleanliness,
            "age": self.age,
            "level": self.level,
            "experience": self.experience
        }

    def get_health(self):
        """gezondheid"""
        return (
            (100 - self.hunger) * 0.25 +
            self.happiness * 0.35 +
            self.energy * 0.25 +
            self.cleanliness * 0.15
        )