import yaml

'''
Configuration keys enumeration
'''


class ConfigKeys:
    DESKS_ARRAY = "desks"
    DESK_ID = "id"
    DESK_NAME = "name"
    DESK_SENSOR_PIN = "sensor_pin"
    DEBUG_MODE = "debug_mode"


''' 
Singleton configuration instance
'''
__config = None

'''
This class is responsible for loading the configuration of the whole program, and
should be responsible for parsing the data so that it is fairly easy to access what we need when using this class
within other classes
'''


class YAMLConfigLoader:
    __yaml_file = ""
    __property_dictionary = {}

    '''
    Initialize Config Loader with config.yaml as default file
    '''
    def __init__(self, yaml_file):
        self.__yaml_file = yaml_file
        self.reload_config()

    '''
    Loads YAML config file. Could potentially change this to SQLite in future,
    so that a user cant go in and just change values (if this is the case, it should still be managed by us)
    '''
    def reload_config(self):

        # Load the file as stream
        with open(self.__yaml_file, 'r') as stream:
            try:
                # Parse YAML. The yaml.load function already puts it into a dictionary, so no conversion is necessary
                self.__property_dictionary = yaml.load(stream)
            except yaml.YAMLError as e:
                print(e)

    '''
    Get property dictionary
    '''
    def get_properties(self):
        return self.__property_dictionary


'''
Using singleton pattern to maintain one single (global) configuration for the whole program.
The input parameter 'yaml_file' will be ignored if the configuration object has already been loaded
'''


def get_global_config(yaml_file="config/config.yaml"):
    global __config

    if not __config:
        __config = YAMLConfigLoader(yaml_file)

    return __config