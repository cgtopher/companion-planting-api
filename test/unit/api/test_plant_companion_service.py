from unittest.mock import Mock

import pytest

from api.plant_companion_service import PlantCompanionService
from api.plant_repository import PlantCompanionRepository
from model.plant import Plant, PlantCategory
from test.conftest import plant_return, valid_plant_request


@pytest.fixture
def repository_returns():
    return [
        Plant('eggplant', PlantCategory.VEG, companions=['corn', 'carrots', 'chard', 'beans']),
        Plant('potato', PlantCategory.VEG, companions=['oregano', 'rosemary', 'mint', 'cabbage']),
        Plant('borage', PlantCategory.VEG, companions=['pumpkin', 'squash']),
        Plant('cucumber', PlantCategory.VEG, companions=['broccoli']),
        Plant('peppers', PlantCategory.VEG, companions=[]),
    ]


@pytest.fixture
def mock_plant_repo(repository_returns):
    repo = PlantCompanionRepository()
    m = Mock()
    m.side_effect = repository_returns
    repo.get_friendliest_plant = m
    return repo


def test_generate_plant_boxes(mock_plant_repo, valid_plant_request, repository_returns, plant_return):
    service = PlantCompanionService(repository=mock_plant_repo)
    results = service.generate_plant_boxes(valid_plant_request)

    assert results is not None
    for i in range(len(results)):
        plant_return[i]['plant_names'].sort()
        results[i].plant_names.sort()
        assert plant_return[i]['plant_names'] == results[i].plant_names
