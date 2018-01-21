from unittest import TestCase
from mock import patch, Mock
from sensors.sensor import Sensor
from sensors.omron_d6t.omron_d6t import OmronD6T

class TestOmronD6T(TestCase):
    def setUp(self):
        with patch.object(Sensor, "__init__", return_value = Mock()):
            self.__omron_d6t = OmronD6T(1, 0xa)

        self.__room_temperature = 25
        self.__temperature_values = [ 25.5, 22.5, 28.9, 26.2,
                                      22.4, 22.2, 29.4, 29.9,
                                      28.4, 23.0, 28.0, 27.7,
                                      22.9, 24.3, 28.8, 27.6 ]

    @patch("sensors.omron_d6t.omron_d6t.OmronD6T._OmronD6T__read")
    def test_occupied_status_is_true(self, mocked_read):
        mocked_read.return_value = (self.__room_temperature, self.__temperature_values)

        self.assertTrue(self.__omron_d6t.occupied_status)

    @patch("sensors.omron_d6t.omron_d6t.OmronD6T._OmronD6T__read")
    def test_occupied_status_is_false(self, mocked_read):
        self.__temperature_values[-1] = self.__room_temperature - 1

        mocked_read.return_value = (self.__room_temperature, self.__temperature_values)

        self.assertFalse(self.__omron_d6t.occupied_status)

    @patch("sensors.sensor.Sensor.read_raw_data")
    def test_read_method_works_properly(self, mocked_read_raw_data):
        # This corresponds to the following temperature tuple
        # (25.7, [22.6, 27.6, 30.5, 23.2, 23.1, 27.5, 29.8, 26.2, 25.1, 27.2, 27.0, 27.3, 26.4, 26.1, 26.5, 26.1])
        mocked_read_raw_data.return_value = (35, bytearray(b'\x01\x01\xe2\x00\x14\x011\x01\xe8\x00\xe7\x00\x13\x01*\x01\x06\x01\xfb\x00\x10\x01\x0e\x01\x11\x01\x08\x01\x05\x01\t\x01\x05\x019'))

        self.assertTrue(self.__omron_d6t.occupied_status)
