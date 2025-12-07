#save_system.py
import json
import os
from settings import SAVE_FILE, DEFAULT_STATS

def save_data(pet):
    """save pet data"""
    data = {
        "hunger": pet.stats["hunger"],
        "energy": pet.stats["energy"],
        "happiness": pet.stats["happiness"],
        "hygiene": pet.stats["hygiene"],
        "age": pet.stats["age"]
    }
    
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)
    
    print(f"data saved to {SAVE_FILE}")

def load_data():
    """load pet data from file return defaults if not exists"""
    if not os.path.exists(SAVE_FILE):
        print(f"no save file found using defaults")
        return DEFAULT_STATS.copy()
    
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        print(f"data loaded from {SAVE_FILE}")
        return data
    except:
        print(f"error loading save file using defaults")
        return DEFAULT_STATS.copy()