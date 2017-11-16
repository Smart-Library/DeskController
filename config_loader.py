import yaml
import os

class _DeskConfigDAO:
    """
    Desk Config DAO
    """

    KEY_ID = "id"
    KEY_NAME = "name"
    KEY_SENSOR_PIN = "sensor_pin"

    def __init__(self, desk):
        self.__desk_id = desk[self.KEY_ID]
        self.__desk_name = desk[self.KEY_NAME]
        self.__desk_pin = desk[self.KEY_SENSOR_PIN]

    @property
    def id(self):
        return self.__desk_id

    @property
    def name(self):
        return self.__desk_name

    @property
    def pin(self):
        return self.__desk_pin


class _DebugConfigDAO:
    """
    Debug Config DAO
    """

    KEY_ENABLED = "enabled"
    KEY_REMOTE_SIMULATOR_CONFIG = "remote-simulator"

    def __init__(self, debug):
        self.__enabled = debug[self.KEY_ENABLED]
        self.__remote_simulator_config = _RemoteSimulatorConfigDAO(debug[self.KEY_REMOTE_SIMULATOR_CONFIG])

    @property
    def enabled(self):
        return self.__enabled

    @property
    def simulator_config(self):
        return self.__remote_simulator_config


class _RemoteSimulatorConfigDAO:
    """
    Simulator Config DAO
    """
    KEY_ENABLED = "enabled"
    KEY_PORT = "port"

    def __init__(self, simulator):
        self.__enabled = simulator[self.KEY_ENABLED]
        self.__port = simulator[self.KEY_PORT]

    @property
    def enabled(self):
        return self.__enabled

    @property
    def port(self):
        return self.__port


class _ConfigDAO:
    """
    Data Access Object (DAO) for the configuration
    """
    KEY_DEBUG_CONFIG = "debug"
    KEY_DESK_CONFIGS = "desks"

    def __init__(self, loader):

        self.__properties = loader

        self.__desks = []
        self.__debug_config = _DebugConfigDAO(self.__properties[self.KEY_DEBUG_CONFIG])

        for desk in self.__properties[self.KEY_DESK_CONFIGS]:
            self.__desks.append(_DeskConfigDAO(desk))

    @property
    def debug_config(self):
        return self.__debug_config

    @property
    def desks(self):
        return self.__desks

    def __str__(self):
        return self.__properties.__str__()


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

        CONFIG = _ConfigDAO(__YAMLConfigLoader(file_name).properties)

        if CONFIG.debug_config.enabled:
            # Print config
            print("[Config]:", CONFIG)

    return CONFIG


# Use a different config if we are currently running in a CI environment
if os.getenv("CI"):
    load_config("config/config_CI.yaml")
else:
    load_config()
