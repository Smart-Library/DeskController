from vcr_unittest import VCRTestCase
from services.desk_handler_service import DeskHandlerService
from config.config import CONFIG

class TestDeskHandlerService(VCRTestCase):
    def test_create_is_successful(self):
        (status, response) = DeskHandlerService.create(name = 'test desk', i2c_address = 15)

        self.assertEqual(status, DeskHandlerService.SUCCESS_STATUS)
        self.assertTrue(self.__find_desk_from_config('test desk'))

    def test_create_is_unsuccessful(self):
        (status, response) = DeskHandlerService.create(name = '', i2c_address = 14)

        self.assertEqual(status, DeskHandlerService.FAILURE_STATUS)
        self.assertFalse(self.__find_desk_from_config(''))

    def __find_desk_from_config(self, name):
        return next((x for x in CONFIG.desks if x.name == name), None)
