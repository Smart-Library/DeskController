import yaml
import os


class _SensorTypeConfigDAO:
    """
    Sensor Type Config DAO
    """

    KEY_TYPE = "type"
    KEY_NAME = "name"

    def __init__(self, sensor):
        self.__sensor_type = sensor[self.KEY_TYPE]
        self.__name = sensor[self.KEY_NAME]

    @property
    def sensor_type(self):
        return self.__sensor_type

    @property
    def sensor_name(self):
        return self.__name

    @property
    def properties(self):
        return {self.KEY_TYPE: self.sensor_type, self.KEY_NAME: self.__name}

    def __str__(self):
        return "Sensor:\n\tType: " + str(self.__sensor_type) + "\n\tName: " + str(self.__name)


class _DeskSensorConfigDAO:
    """
    Desk Sensor Config DAO
    """

    KEY_TYPE = "type"
    KEY_BUS = "i2c_bus"
    KEY_ADDRESS = "i2c_address"

    def __init__(self, desk):
        self.__sensor_type = desk[self.KEY_TYPE]
        self.__i2c_bus = desk[self.KEY_BUS]
        if type(desk[self.KEY_ADDRESS]) is int:
            self.__i2c_address = desk[self.KEY_ADDRESS]
        else:
            self.__i2c_address = int(desk[self.KEY_ADDRESS], 16)

    @property
    def sensor_type(self):
        return self.__sensor_type

    @property
    def i2c_bus(self):
        return self.__i2c_bus

    @property
    def i2c_address(self):
        return self.__i2c_address

    @sensor_type.setter
    def sensor_type(self, sens_type):
        if type(sens_type) is int:
            self.__sensor_type = sens_type

    @i2c_bus.setter
    def i2c_bus(self, bus):
        if type(bus) is int:
            self.__i2c_bus = bus

    @i2c_address.setter
    def i2c_address(self, addr):
        if type(addr) is int:
            self.__i2c_address = addr

    @property
    def properties(self):
        return {self.KEY_TYPE: self.__sensor_type, self.KEY_BUS: self.__i2c_bus,
                self.KEY_ADDRESS: "0x{:02X}".format(self.__i2c_address)}

    def __str__(self):
        return "Desk Sensor:\n\t\tType: " + str(self.__sensor_type) + "\n\t\ti2c_bus: " + str(self.__i2c_bus) + \
               "\n\t\ti2c_address: " + hex(self.__i2c_address)


class _DeskConfigDAO:
    """
    Desk Config DAO
    """

    KEY_ID = "id"
    KEY_NAME = "name"
    KEY_SENSOR = "sensor"

    def __init__(self, desk):
        self.__desk_id = desk[self.KEY_ID]
        self.__desk_name = desk[self.KEY_NAME]
        self.__desk_sensor = _DeskSensorConfigDAO(desk[self.KEY_SENSOR])

    @property
    def id(self):
        return self.__desk_id

    @property
    def name(self):
        return self.__desk_name

    @property
    def sensor(self):
        return self.__desk_sensor

    @id.setter
    def id(self, desk_id):
        if type(desk_id) is int:
            self.__desk_id = desk_id

    @name.setter
    def name(self, desk_name):
        if type(desk_name) is str:
            self.__desk_id = desk_name

    @property
    def properties(self):
        return {self.KEY_ID: self.__desk_id, self.KEY_NAME: self.__desk_name, self.KEY_SENSOR: self.__desk_sensor.properties}

    def __str__(self):
        return "Desk:\n\tID: " + str(self.__desk_id) + "\n\tName: " + str(self.__desk_name) + "\n\t" \
               + str(self.__desk_sensor)


class _DebugConfigDAO:
    """
    Debug Config DAO
    """

    KEY_ENABLED = "enabled"

    def __init__(self, debug):
        self.__enabled = debug[self.KEY_ENABLED]

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, enabled):
        if type(enabled) is bool:
            self.__enabled = enabled

    @property
    def properties(self):
        return {self.KEY_ENABLED: self.enabled}

    def __str__(self):
        return "Debug Config: \n\tEnabled: " + str(self.enabled)


class _ConfigDAO:
    """
    Data Access Object (DAO) for the configuration
    """
    __KEY_DEBUG_CONFIG = "debug"
    __KEY_DESKS_CONFIG = "desks"
    __KEY_SENSORS_CONFIGS = "sensors"

    def __init__(self, loader):
        self.__loader = loader
        self.__properties = loader.properties

        # Initialize
        self.__desks = []
        self.__sensors = []
        self.__debug_config = None

        # Load fields from config properties
        self.load_config_objects()

    def load_config_objects(self):
        self.__debug_config = _DebugConfigDAO(self.__properties[self.__KEY_DEBUG_CONFIG])

        # Reload Sensors
        self.__sensors.clear()
        for sensor in self.__properties[self.__KEY_SENSORS_CONFIGS]:
            self.__sensors.append(_SensorTypeConfigDAO(sensor))

        # Reload desks
        self.__desks.clear()
        for desk in self.__properties[self.__KEY_DESKS_CONFIG]:
            self.__desks.append(_DeskConfigDAO(desk))

    def reload(self):
        """
        Reload global application configuration
        """
        # Load newest config
        self.__loader.load_config()
        self.__properties = self.__loader.properties
        self.load_config_objects()

    def save(self):
        """
        Saves current config to file
        """
        self.__loader.save_config()

    @property
    def debug_config(self):
        return self.__debug_config

    @property
    def desks(self):
        return self.__desks

    @property
    def sensors(self):
        return self.__sensors

    def add_desk(self, desk_id, name, sensor_address, sensor_type=1, sensor_bus=1):
        # Get latest config file
        self.reload()

        # Set new sensor info
        new_sensor = {_DeskSensorConfigDAO.KEY_TYPE: sensor_type,
                      _DeskSensorConfigDAO.KEY_BUS: sensor_bus,
                      _DeskSensorConfigDAO.KEY_ADDRESS: sensor_address}

        # Create new desk config with sensor info
        new_desk = _DeskConfigDAO({_DeskConfigDAO.KEY_ID: desk_id,
                                   _DeskConfigDAO.KEY_NAME: name,
                                   _DeskConfigDAO.KEY_SENSOR: new_sensor})
        # Append and save config
        self.__desks.append(new_desk)
        self.save()

    @property
    def properties(self):
        desks = []
        sensors = []

        for desk in self.__desks:
            desks.append(desk.properties)

        for sensor in self.__sensors:
            sensors.append(sensor.properties)

        return {self.__KEY_DEBUG_CONFIG: self.__debug_config.properties, self.__KEY_DESKS_CONFIG: desks, self.__KEY_SENSORS_CONFIGS: sensors}

    def __str__(self):
        ret = "Loaded Configuration:\n\n" + str(self.__debug_config) + "\n"
        for d in self.__desks:
            ret += str(d)
            ret += "\n"

        for s in self.__sensors:
            ret += str(s)
            ret += "\n"

        return ret


class __YAMLConfigLoader:
    """
    YAML Configuration Loader
    """

    def __init__(self, yaml_file):
        """
        Loads YAML config file
        :param yaml_file: Path to YAML file
        """

        self.__property_dictionary = {}
        self.__yaml_file = yaml_file
        self.load_config()

    def load_config(self):
        """
        Loads YAML config file.
        :return: None
        """

        # Load the file as stream
        with open(self.__yaml_file, 'r') as stream:
            try:
                # Parse YAML. The yaml.load function already puts it into a dictionary, so no conversion is necessary
                self.__property_dictionary = yaml.load(stream)
            except yaml.YAMLError as e:
                print(e)
                raise e

    def save_config(self):
        with open(self.__yaml_file, 'w') as stream:
            try:
                stream.write(yaml.dump(CONFIG.properties, default_flow_style=False))
            except yaml.YAMLError as e:
                print(e)
                raise e

    @property
    def properties(self):
        """
        Get property dictionary
        :return: Property Dictionary
        """

        return self.__property_dictionary


# Global Config DAO available for access via import
# Should be initialized when this module is imported
CONFIG: _ConfigDAO = None


def load_config(file_name="config/config.yaml"):
    """
    This method ensures that we only load the config once.
    :return: The global Config DAO
    """
    global CONFIG

    if not CONFIG:
        CONFIG = _ConfigDAO(__YAMLConfigLoader(file_name))

    return CONFIG



# Use a different config if we are currently running in a CI environment
if os.getenv("CI"):
    load_config("tests/config/config.yaml")
else:
    load_config()