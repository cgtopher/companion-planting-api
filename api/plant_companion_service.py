from typing import List

from api.plant_repository import PlantCompanionRepository
from model.dto import BoxDTO, PlantDTO


class PlantCompanionService:
    def __init__(self, **kwargs):
        self.repository: PlantCompanionRepository = kwargs.get('repository') or PlantCompanionRepository()

    def get_all(self) -> List[PlantDTO]:
        return [PlantDTO(p.name, p.friendly_name) for p in self.repository.get_all_plants()]


    '''
        Pretty simple algo for now,
        - Get plant with most companions in list
        - Get companions for that plant filtering out any who don't work well together (:AVOID relationship between them)
        - Put that plant and its companions in a 'box'
        - Rinse and repeat with remaining plants
        
       Other ideas could be to be more pessimistic with matching, perhaps adding
       a threshold, maybe user defined, for how many plants max can be in a box, 
       and optimize for that in the query, which might? end up with more balanced boxes.
       Or allowing the user to pick out the initial 'head' plants to be chosen first if there
       is some other unknown consideration
    
        This isn't going to be an ideal planting situation on it's own, for now it just identifies
        companion plants and who they should avoid. Planning on getting more data around other kinds of 
        relationships to make better decisions such as:
        - Prioritizing the "three sisters" grouping of beans, squash, and corn
        - Considering the seasons each plant is harvested at to make groupings of opposing harvest times
            to more efficiently use space
        - Considering the 'extent' to which plants help each other, for instance marigolds help many plants
            but tomatoes because of their pest deterrence ability
        - Taking region into account to perhaps suggest plants that will help with local pests, or just grow better
            
    '''
    def generate_plant_boxes(self, plant_names: List[str]) -> List[BoxDTO]:
        unassigned = plant_names
        boxes: List[BoxDTO] = []
        while len(unassigned) > 0:
            plant = self.repository.get_friendliest_plant(unassigned)
            box = plant.make_box(unassigned)
            boxes.append(box)
            unassigned = list(set(unassigned).difference(box.plant_names))

        return boxes
