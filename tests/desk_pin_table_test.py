import unittest
import desk_sensors


class DeskPinTableTest(unittest.TestCase):

    def setUp(self):
        self.__desk_pin_table = desk_sensors.DeskPinTable()

    def test_valid_get_mapping_from_desk_id(self):
        (pin, desk_obj) = self.__desk_pin_table.get_mapping_from_desk_id(1)
        self.assertEqual(desk_obj.desk_id, 1)
        self.assertEqual(pin, 2)

        (pin, desk_obj) = self.__desk_pin_table.get_mapping_from_desk_id(2)
        self.assertEqual(desk_obj.desk_id, 2)
        self.assertEqual(pin, 3)

    def test_invalid_get_mapping_from_desk_id(self):
        ret_obj = self.__desk_pin_table.get_mapping_from_desk_id(-1)
        self.assertEqual(ret_obj, None)

        ret_obj = self.__desk_pin_table.get_mapping_from_desk_id(3)
        self.assertEqual(ret_obj, None)
