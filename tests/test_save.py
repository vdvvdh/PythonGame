#tests
from save_system import save_data, load_data
from pet import Pet
from settings import SAVE_FILE
import os
import json

def test_save_and_load():
    pet = Pet()
    pet.stats["hunger"] = 33

    save_data(pet)
    data = load_data()

    assert data["hunger"] == 33

def test_missing_save_file():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

    data = load_data()
    assert "hunger" in data
