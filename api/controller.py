from flask import Flask, request, Blueprint
import json

from api.plant_companion_service import PlantCompanionService
from model.dto import PlantListingDTO

companion_plant_controller = Blueprint('companion_plant_controller', __name__)

service = PlantCompanionService()
app = companion_plant_controller


@app.route("/", methods=['GET'])
def get_all():
    plants = service.get_all()
    return PlantListingDTO(plants).to_dict()

@app.route('/boxes', methods=['POST'])
def generate_companion_boxes():
    plant_list = json.loads(request.data)['plant_list']
    boxes = service.generate_plant_boxes(plant_list)
    return {'boxes': [b.to_dict() for b in boxes]}
