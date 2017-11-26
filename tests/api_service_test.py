from vcr_unittest import VCRTestCase
from api_service import ApiService

class TestApiService(VCRTestCase):

    def test_create_desk_is_successful(self):
        response = ApiService.create_desk(name = 'test desk')
        json_response = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in json_response)
        self.assertEqual('test desk', json_response['name'])

    def test_update_desk_occupied_status_is_successful(self):
        response = ApiService.update_desk_occupied_status(id = 1, occupied_status = True)
        self.assertEqual(response.status_code, 204)
