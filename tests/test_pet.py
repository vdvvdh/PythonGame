import pytest
from pet import Pet
from settings import DEFAULT_STATS

class TestPet:
    """Tests"""

    def test_default_initialization(self):
        """kijk of een nieuwe pet met standaardinstellingen correct wordt aangemaakt"""
        pet = Pet()
        assert pet.name == "Kitsune"
        assert 0 <= pet.hunger <= 100
        assert 0 <= pet.happiness <= 100
        assert 0 <= pet.energy <= 100
        assert 0 <= pet.cleanliness <= 100
        assert pet.level == 1
        assert pet.age == 0

    def test_custom_initialization(self):
        """Kijk of een pet met aangepaste stats correct wordt geladen"""
        custom_stats = {
            "name": "Test",
            "hunger": 75,
            "happiness": 60,
            "energy": 40,
            "cleanliness": 80,
            "level": 5,
            "age": 100
        }
        pet = Pet(stats=custom_stats)
        assert pet.name == "Test"
        assert pet.hunger == 75
        assert pet.level == 5
        assert pet.age == 100

    def test_feed_reduces_hunger(self):
        """Voeren moet honger verlagen"""
        pet = Pet()
        pet.hunger = 80
        initial = pet.hunger
        result = pet.feed()
        assert result
        assert pet.hunger < initial
        assert pet.hunger >= 0

    def test_feed_boosts_happiness(self):
        """Voeren verhoogt het geluk van de pet"""
        pet = Pet()
        pet.hunger = 80
        initial = pet.happiness
        pet.feed()
        assert pet.happiness >= initial

    def test_feed_when_not_hungry(self):
        """Voeren werkt niet als de pet al bijna vol is"""
        pet = Pet()
        pet.hunger = 5
        result = pet.feed()
        assert result is False

    def test_play_reduces_energy(self):
        """Spelen kost energie"""
        pet = Pet()
        pet.energy = 80
        initial = pet.energy
        result = pet.play()
        assert result
        assert pet.energy < initial

    def test_play_boosts_happiness(self):
        """Spelen maakt de pet blijer"""
        pet = Pet()
        pet.energy = 80
        initial = pet.happiness
        pet.play()
        assert pet.happiness > initial

    def test_play_when_tired(self):
        """Te moe, spelen werkt niet"""
        pet = Pet()
        pet.energy = 5
        result = pet.play()
        assert result is False

    def test_clean_increases_cleanliness(self):
        """Wassen verhoogt de hygiëne"""
        pet = Pet()
        pet.cleanliness = 30
        initial = pet.cleanliness
        result = pet.clean()
        assert result
        assert pet.cleanliness > initial

    def test_clean_when_already_clean(self):
        """Als de pet al schoon is, werkt wassen niet"""
        pet = Pet()
        pet.cleanliness = 90
        result = pet.clean()
        assert result is False

    def test_stats_stay_in_bounds(self):
        """Alle stats blijven tussen 0 en 100"""
        pet = Pet()
        for _ in range(10):
            pet.feed()
            pet.clean()
        assert 0 <= pet.hunger <= 100
        assert 0 <= pet.happiness <= 100
        assert 0 <= pet.energy <= 100
        assert 0 <= pet.cleanliness <= 100

    def test_experience_and_leveling(self):
        """Pet kan levelen door ervaring te verdienen"""
        pet = Pet()
        old_level = pet.level
        for _ in range(15):
            pet.feed()
        assert pet.level > old_level or pet.experience > 0

    def test_mood_happy(self):
        """Mood moet 'happy' zijn bij veel geluk"""
        pet = Pet()
        pet.happiness = 90
        pet.energy = 80
        pet.cleanliness = 70
        assert pet.get_mood() == "happy"

    def test_mood_sad(self):
        """Mood moet 'sad' zijn bij weinig geluk"""
        pet = Pet()
        pet.happiness = 20
        pet.energy = 80
        pet.cleanliness = 70
        assert pet.get_mood() == "sad"

    def test_mood_tired(self):
        """Mood moet 'tired' zijn bij lage energie"""
        pet = Pet()
        pet.happiness = 50
        pet.energy = 20
        pet.cleanliness = 70
        assert pet.get_mood() == "tired"

    def test_mood_dirty(self):
        """Mood moet 'dirty' zijn bij lage hygiëne"""
        pet = Pet()
        pet.happiness = 50
        pet.energy = 80
        pet.cleanliness = 30
        assert pet.get_mood() == "dirty"

    def test_get_stats_returns_dict(self):
        """get_stats geeft een dictionary terug"""
        pet = Pet()
        stats = pet.get_stats()
        assert isinstance(stats, dict)
        for key in ["name", "hunger", "happiness", "energy", "cleanliness", "level"]:
            assert key in stats

    def test_health_calculation(self):
        """Gezondheid berekening klopt"""
        pet = Pet()
        pet.hunger = 0
        pet.happiness = 100
        pet.energy = 100
        pet.cleanliness = 100
        assert pet.get_health() == 100

    def test_status_returns_string(self):
        """get_status geeft een string terug"""
        pet = Pet()
        status = pet.get_status()
        assert isinstance(status, str)
        assert len(status) > 0

class TestSaveSystem:
    """Tests voor save en load"""

    def test_save_and_load(self):
        """Pet opslaan en terugladen werkt"""
        from save_system import save_data, load_data
        import os
        from settings import SAVE_FILE

        pet = Pet()
        pet.hunger = 42
        pet.happiness = 73
        pet.energy = 88
        pet.level = 3

        save_data(pet)
        assert os.path.exists(SAVE_FILE)

        stats = load_data()
        assert stats["hunger"] == 42
        assert stats["happiness"] == 73
        assert stats["energy"] == 88
        assert stats["level"] == 3

        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])