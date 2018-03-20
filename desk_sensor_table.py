from config.config import CONFIG
from desk import Desk
from sensors.omron_d6t.omron_d6t import OmronD6T


class DeskSensorTable:
    """
    This class is responsible for mapping desk objects to Sensors, and polling sensors occupancy data
    """

    def __init__(self):
        """
        Initialize the DeskPinTable object. Register all pin event callbacks
        """

        # In this mapping, each key is a desk ID, and the value is a tuple
        # containing the respective sensor object, and the respective desk object.
        # The sensor object is the object responsible for reading sensor data and reporting occupancy status
        # The desk object is used for performing additional operations on the desk, if necessary.
        self.__desk_dict = {}

        # Load desk dictionary from configuration
        self.__load_desk_dictionary()

    def __load_desk_dictionary(self):
        """
        Load the config file and initialize the desk mapping object
        :return: None
        """

        # Get info for each desk
        for d in CONFIG.desks:

            # Initialize sensor
            sensor_obj = OmronD6T(d.sensor.i2c_bus, d.sensor.i2c_address)

            # Append id, pin, desk object to map
            self.__desk_dict[d.id] = (sensor_obj, Desk(d.name, d.id))

            # Print additional information in debug mode
            if CONFIG.debug_config.enabled:
                print(f"Added Desk to DeskSensorTable: [ID]: {d.id}, [Name]: {d.name}, [Sensor Type]: {d.sensor.sensor_type}")

    def poll_desk_occupancy(self):
        """
        This method is used for polling each sensor for it's occupied status and updating the respective desk
        :return: None
        """
        for (sensor_obj, desk_obj) in self.__desk_dict.values():
            status = sensor_obj.occupied_status
            print(status)
            desk_obj.input_received(status)

    def get_mapping_from_desk_id(self, desk_id):
        """
        Lookup desk information given it's ID
        :param desk_id: The Desk ID to look for
        :return: A tuple containing the sensor object and a Desk object if the ID corresponds to a Desk, or None
        """

        # Ensure None is returned when KeyError is thrown
        # (Occurs if desk_id does not exist)
        try:
            return self.__desk_dict[desk_id]
        except KeyError:
            return None

    def add_observer_to_all_desks(self, obs):
        for (sensor_obj, desk) in self.__desk_dict.values():
            desk.add_observer(obs)

    def cleanup(self):
        # Close all i2c connections
        for (sensor_obj, desk_obj) in self.__desk_dict.values():
            print(f"Closing i2c connection for desk: {desk_obj.desk_id}")
            sensor_obj.close_connection()
