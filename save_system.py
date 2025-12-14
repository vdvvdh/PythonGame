import json
import os
from datetime import datetime

SAVE_FILE = "pet_save.json"

DEFAULT_STATS = {
    "name": "Kitsune",
    "hunger": 50,
    "happiness": 50,
    "energy": 50,
    "cleanliness": 50,
    "age": 0,
    "level": 1,
    "experience": 0
}

def save_data(pet):
    """save pet data to file"""
    data = {
        "name": pet.name,
        "hunger": pet.hunger,
        "energy": pet.energy,
        "happiness": pet.happiness,
        "cleanliness": pet.cleanliness,
        "age": pet.age,
        "level": pet.level,
        "experience": pet.experience,
        "last_saved": datetime.now().isoformat()
    }
    
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"✓ data opgeslagen naar {SAVE_FILE}")
        return True
    except Exception as e:
        print(f"✗ fout bij opslaan: {e}")
        return False

def load_data():
    """load pet data from file, return defaults if not exists"""
    if not os.path.exists(SAVE_FILE):
        print(f"no save file found using defaults")
        return DEFAULT_STATS.copy()
    
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        
        if "last_saved" in data:
            last_saved = datetime.fromisoformat(data["last_saved"])
            hours_passed = (datetime.now() - last_saved).total_seconds() / 3600
            
            if hours_passed > 24:
                print(f"⚠ Save is {int(hours_passed)} uur oud")
                data = apply_time_decay(data, hours_passed)
        
        print(f"✓ Data geladen van {SAVE_FILE}")
        return data
    except Exception as e:
        print(f"✗ Fout bij laden: {e}, gebruik defaults")
        return DEFAULT_STATS.copy()

def apply_time_decay(data, hours_passed):
    """apply stat decay for time passed"""
    decay_factor = min(hours_passed / 24, 0.5)
    
    data["hunger"] = min(100, data.get("hunger", 50) + (30 * decay_factor))
    data["energy"] = max(0, data.get("energy", 50) - (30 * decay_factor))
    data["cleanliness"] = max(0, data.get("cleanliness", 50) - (20 * decay_factor))
    data["happiness"] = max(0, data.get("happiness", 50) - (20 * decay_factor))
    
    return data

def delete_save():
    """delete save file"""
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
            print(f"✓ Save file verwijderd")
            return True
        except Exception as e:
            print(f"✗ Fout bij verwijderen: {e}")
            return False
    return False

def save_exists():
    """check if save exists"""
    return os.path.exists(SAVE_FILE)