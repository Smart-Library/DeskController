from unittest import TestCase
from mock import patch, Mock
from sensors.sensor import Sensor

class TestOmronD6T(TestCase):
    @patch("pigpio.pi", return_value = Mock())
    @patch("sensors.sensor.Sensor.open_connection", return_value = 1)
    @patch("sensors.sensor.Sensor.write_raw_data", return_value = True)
    def setUp(self, mocked_pigpio, mocked_open_connection, mocked_write_raw_data):
        mocked_pigpio.connected = True
        self.__sensor = Sensor(bus = 1, address = 14, start_command = 0x4c, buffer_length = 35)

    def test_occupied_status_raises_exception(self):
        with self.assertRaises(NotImplementedError):
            self.__sensor.occupied_status
