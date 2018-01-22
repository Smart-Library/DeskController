import crcmod.predefined as crcmod
from time import sleep
from sensors.sensor import Sensor

class OmronD6T(Sensor):
    __START_COMMAND = 0x4c
    __I2C_ADDRESS = 0x0a
    __ARRAY_SIZE = 16
    __BUFFER_LENGTH = 35
    __PEC_PREFIX = 0x15
    __MAX_CELLS_ABOVE_ROOM_TEMPERATURE = 10

    def __init__(self, bus = 1, address = None):
        if not address: address = self.__I2C_ADDRESS
        super().__init__(bus = bus, address = address, start_command = self.__START_COMMAND, buffer_length = self.__BUFFER_LENGTH)

    @property
    def occupied_status(self):
        room_temperature, temperature_matrix = self.__read()

        return self.__temperature_cells_above_threshold(room_temperature, temperature_matrix) >= self.__MAX_CELLS_ABOVE_ROOM_TEMPERATURE

    def __temperature_cells_above_threshold(self, room_temperature, temperature_array):
        """
        :param room_temperature: Room temperature
        :param temperature_array: Temperature list from sensor

        :return: Number of cells above room temperature 
        """
        return sum(temperature > room_temperature for temperature in temperature_array)

    def __read(self):
        """
        Read sensor data and parse it appropriately. Checks PEC to ensure the data is valid.

        :return: Tuple containing room temperature and an array of measured temperatures, or None if there was an issue
        reading from the sensor
        """

        # This loop will run until a valid value is received from the sensor (or max retries is reached)
        for i in range(0, self.MAX_RETRIES):
            bytes_read, sensor_raw_data = self.read_raw_data()

            if bytes_read == self.__BUFFER_LENGTH:
                # Read PEC byte for checksum
                crc_expected = sensor_raw_data[34]

                # Calculate CRC-8 of received bytes (excluding PEC byte at end)
                crc_actual = self.__compute_crc(sensor_raw_data[:34])

                if crc_expected == crc_actual:
                    # Number of bytes read, and CRC is correct -> Parse Temperature data
                    return self.__parse_temperature_data(sensor_raw_data)
                else:
                    # Wait between retries
                    sleep(0.05)
                    continue
            else: # Handle i2c error transmissions
                print('\n[Error]: Number of bytes mismatch. Number of bytes read: ' + str(bytes_read))

                # Wait between retries
                sleep(0.05)
                continue

        return None

    def __parse_temperature_data(self, raw_sensor_buffer):
        if len(raw_sensor_buffer) != self.__BUFFER_LENGTH:
            return None

        # Read low + high byte of room temperature
        t = (raw_sensor_buffer[1] << 8) | raw_sensor_buffer[0]
        room_temperature = t / 10

        # Read low + high byte of pixel temperatures (16 total pixels = 32 total bytes) into empty array
        cur_pixel = 0
        temperature = [0.0] * self.__ARRAY_SIZE

        # See Omron D6T Datasheet. Reads through low & high bytes of temperature data
        for j in range(2, len(raw_sensor_buffer) - 2, 2):
            temperature[cur_pixel] = ((raw_sensor_buffer[j + 1] << 8) | raw_sensor_buffer[j]) / 10
            cur_pixel += 1

        return room_temperature, temperature

    def __compute_crc(self, buf):
        crc8_func = crcmod.mkCrcFun('crc-8')

        # See OMRON datasheet for PEC details
        pec_buffer = [self.__PEC_PREFIX]

        for itm in buf:
            pec_buffer.append(itm)

        return crc8_func(bytearray(pec_buffer))
