import pytest
from pet import Pet

def test_pet_feeding():
    pet = Pet()
    original_hunger = pet.stats["hunger"]
    pet.feed()
    assert pet.stats["hunger"] < original_hunger

def test_pet_play():
    pet = Pet()
    original_happiness = pet.stats["happiness"]
    original_energy = pet.stats["energy"]
    pet.play()
    assert pet.stats["happiness"] > original_happiness
    assert pet.stats["energy"] < original_energy

def test_clamp():
    pet = Pet()
    assert pet.clamp(-10) == 0
    assert pet.clamp(150) == 100
