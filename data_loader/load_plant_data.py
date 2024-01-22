import csv

from model.plant import Plant, PlantCategory
from neo4j_driver_manager import Neo4JDriverManager

'''
    Read plants data from a csv and loads them into Neo4J
    
    Follow the formatting in the included companionplants.csv, the Companions and Avoid columns 
    are comma separated lists of plants that MUST be in the Name column with the same
    spelling, which acts as a sort of foreign key for establishing the respective relationships,
    or you could get unexpected results from your queries.
    
    This script is idempotent, so you can simply add a plant to the csv and rerun it
'''
def load_plant_data(file: str):
    data = _read_companion_plant_data(file)
    _write_companion_plant_data(data)


def _read_companion_plant_data(file: str) -> list[Plant]:
    data = []
    with open(file, 'r') as companion_plant_data:
        reader = csv.reader(companion_plant_data)
        for row in reader:
            # header condition
            if row[0] == 'Category':
                continue

            # Name, Companions, Avoid
            for i in [1, 3, 4]:
                row[i] = row[i].lower()

            data.append(Plant(row[1], PlantCategory[row[0].upper()], companions=row[3].split('|'), avoids=row[4].split('|')))

        companion_plant_data.close()

    return data


def _write_companion_plant_data(data: list[Plant]):
    manager = Neo4JDriverManager()

    transaction = manager.get_transaction()
    try:
        for plant in data:
            transaction.run(f'''
                MERGE (p:Plant {{ name: "{plant.name}", category: "{plant.category.value}" }} )
                ON MATCH
                    SET p.friendlyName = "{plant.friendly_name}"
                ON CREATE
                    SET p.friendlyName = "{plant.friendly_name}"
            ''')
        transaction.commit()
    except Exception as e:
        transaction.rollback()
        raise e

    transaction = manager.get_transaction()
    try:
        for plant in data:
            # Assuming relations go both ways to account for human error (like my own) using MERGE gives safety
            # around running the same relationship multiple times
            transaction.run(f'''
                MATCH (p:Plant) WHERE p.name = "{plant.name}"
                MATCH (c:Plant) WHERE c.name IN ['{"','".join(plant.companions)}']
                MATCH (a:Plant) WHERE a.name IN ['{"','".join(plant.avoids)}']
                MERGE (p)-[:COMPANION]->(c)
                MERGE (c)-[:COMPANION]->(p)
                MERGE (p)-[:AVOID]->(a)
                MERGE (a)-[:AVOID]->(p)
            ''')

        transaction.commit()
    except Exception as e:
        transaction.rollback()
        raise e


load_plant_data("data/companionplants-20240117.csv")
