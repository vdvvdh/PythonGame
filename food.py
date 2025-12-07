#food.py

class Food:
    def __init__(self, name, hunger_reduction, happiness_boost=0):
        self.name = name
        self.hunger_reduction = hunger_reduction
        self.happiness_boost = happiness_boost
