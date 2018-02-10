import unittest
import desk_sensor_table
from mock import patch, Mock


class DeskPinTableTest(unittest.TestCase):

    @patch("pigpio.pi", return_value=Mock())
    @patch("sensors.sensor.Sensor.open_connection", return_value=1)
    @patch("sensors.sensor.Sensor.write_raw_data", return_value=True)
    def setUp(self, mocked_pigpio, mocked_open_connection, mocked_write_raw_data):
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
