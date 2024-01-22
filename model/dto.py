from typing import List


class PlantDTO:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class PlantListingDTO:
    def __init__(self, plants: List[PlantDTO]):
        self.plants = plants

    def to_dict(self):
        return {
            'plants': [p.to_dict() for p in self.plants]
        }

class BoxDTO:
    def __init__(self, plant_names: List[str]):
        self.plant_names = plant_names

    def to_dict(self):
        return {
            'plant_names': self.plant_names
        }

