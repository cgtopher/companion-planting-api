from enum import Enum
from typing import List

from model.dto import BoxDTO


class PlantCategory(Enum):
    VEG = "veg"
    HRB = "hrb"




class Plant:
    def __init__(self, name, category: PlantCategory, **kwargs):
        self.name: str = name
        self.category: PlantCategory = category
        self.friendly_name: str = kwargs.get('friendly_name') or None
        self.companions: List[str] = kwargs.get('companions') or []
        self.avoids:List[str] = kwargs.get('avoids') or []

    def make_box(self, plants: List[str]) -> BoxDTO:
        companions = list(set(plants).intersection(self.companions))
        companions.append(self.name)
        return BoxDTO(companions)
