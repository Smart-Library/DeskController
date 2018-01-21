import unittest
import desk_sensor_table


class DeskPinTableTest(unittest.TestCase):

    def setUp(self):
        self.__desk_pin_table = desk_sensor_table.DeskSensorTable()

    def test_valid_get_mapping_from_desk_id(self):
        (sensor_obj, desk_obj) = self.__desk_pin_table.get_mapping_from_desk_id(1)
        self.assertEqual(desk_obj.desk_id, 1)
        self.assertIsNotNone(sensor_obj)

        (sensor_obj, desk_obj) = self.__desk_pin_table.get_mapping_from_desk_id(2)
        self.assertEqual(desk_obj.desk_id, 2)
        self.assertIsNotNone(sensor_obj)

    def test_invalid_get_mapping_from_desk_id(self):
        ret_obj = self.__desk_pin_table.get_mapping_from_desk_id(-1)
        self.assertEqual(ret_obj, None)

        ret_obj = self.__desk_pin_table.get_mapping_from_desk_id(3)
        self.assertEqual(ret_obj, None)
