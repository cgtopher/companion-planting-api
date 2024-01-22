import pytest


@pytest.fixture(autouse=True, scope="session")
def valid_plant_request():
    return ["beans", "carrots", "cucumber", "mint", "corn", "eggplant", "chard", "rosemary", "borage", "squash",
            "oregano", "peppers", "broccoli", "cabbage", "pumpkin", "potato"]


@pytest.fixture(autouse=True, scope="session")
def plant_return():
    return [
        {
            "plant_names": [
                "eggplant",
                "corn",
                "carrots",
                "chard",
                "beans"
            ]
        },
        {
            "plant_names": [
                "potato",
                "oregano",
                "rosemary",
                "mint",
                "cabbage"
            ]
        },
        {
            "plant_names": [
                "borage",
                "pumpkin",
                "squash"
            ]
        },
        {
            "plant_names": [
                "cucumber",
                "broccoli"
            ]
        },
        {
            "plant_names": [
                "peppers"
            ]
        }
    ]
