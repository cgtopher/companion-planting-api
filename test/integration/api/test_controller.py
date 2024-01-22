from test.conftest import valid_plant_request, plant_return

'''
    Will add a test containers set up for this, for now assumes neo4j is running and load_data has been run,
    which will all be automated to make sure we're getting the expected responses
'''


def test_generate_companion_boxes(client, valid_plant_request, plant_return):
    response = client.post('/companions/boxes', json={
        'plant_list': valid_plant_request
    })

    assert response.status_code == 200
    for i in range(len(response.json['boxes'])):
        expected = plant_return[i]['plant_names']
        expected.sort()
        actual = response.json['boxes'][i]['plant_names']
        actual.sort()
        assert expected == actual

