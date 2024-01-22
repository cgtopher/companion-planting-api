from typing import List

import pandas as pd

from model.plant import Plant, PlantCategory
from neo4j_driver_manager import Neo4JDriverManager


class PlantCompanionRepository():
    def __init__(self):
        self.driver_manager = Neo4JDriverManager()


    def get_all_plants(self) -> List[Plant]:
        result = self.driver_manager.execute_query(f'''
            MATCH (p:Plant) RETURN p as plant
        ''')

        return [Plant(p['name'], PlantCategory[p['category'].upper()], friendly_name=p['friendlyName']) for p in result['plant']]

    def get_friendliest_plant(self, plants: List[str]) -> Plant:
        plant_result = self.driver_manager.execute_query(f'''
                MATCH (p:Plant) WHERE p.name in ['{"','".join(plants)}']
                RETURN p as plant, count {{(p)-[:COMPANION]->(c) where c.name in ['{"','".join(plants)}']}} as companionCount
                ORDER BY companionCount desc
                LIMIT 1
            ''')

        if plant_result.size == 0:
            raise Exception('No plants found, only use supported plant names')

        head_plant = plant_result['plant'][0]

        companions = self._get_companions(head_plant['name'], plants)

        return Plant(head_plant['name'], PlantCategory[head_plant['category'].upper()], companions=[c['name'] for c in companions])

    def _get_companions(self, head_plant: str, available_plants: List[str]) -> List[str]:
        '''
            Might try to figure out whether I can collapse these queries. In testing, I found
            that I can't query for 'a' without affecting the results of 'c'. One option might be
            trying some magic with a COLLECT {}
        '''
        avoid_result = self.driver_manager.execute_query(f'''
            MATCH (p:Plant)-[:COMPANION]->(c:Plant)<-[:AVOID]-(a:Plant)<-[:COMPANION]-(p)
                WHERE p.name = '{head_plant}' 
                AND c.name in ['{"','".join(available_plants)}']
                AND a.name in ['{"','".join(available_plants)}']
            RETURN a as avoid
        ''')

        companion_result = self.driver_manager.execute_query(f'''
            MATCH (p:Plant)-[:COMPANION]->(c:Plant)
                WHERE p.name = '{head_plant}' 
                AND c.name in ['{"','".join(available_plants)}']
            RETURN c as companion
        ''')
        avoid_map = {a['name']: True for a in avoid_result['avoid']}

        companions = []
        # since the df comes out as [ index | Node object ] we can't use
        # df's nice .loc() method. At least loading the lookup into a dict
        # to avoid possible O(n^2)
        for c in companion_result['companion']:
            if not avoid_map.get(c['name']):
                companions.append(c)

        return companions


