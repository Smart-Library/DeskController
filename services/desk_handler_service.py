from config.config import CONFIG
from services.api_service import ApiService

class DeskHandlerService:
    """
    This class will be responsible for communicating with the ApiService and the CONFIG global
    to handle all desk related operations
    """
    SUCCESS_STATUS = "success"
    FAILURE_STATUS = "failure"
    SUCCESSFUL_CREATE = "Success! You can see your newly created desk in config/config.yaml"
    FAILED_CREATE = "Uh oh! We couldn't create the desk with the inputs you provided.\nPlease review your inputs and try again."

    @classmethod
    def create(cls, name, i2c_address):
        """
        This method creates a desk on both the API side and the local config side.

        :param name: Name of desk
        :param i2c_address: Address of desk on the I2C bus
        :return: A tuple containing a status flag and the json response from our API
        """
        response = ApiService.create_desk(name)
        json_response = response.json()
        if response.status_code == 201:
            CONFIG.update_desk_list({'name': name, 'id': json_response['id'], 'sensor_pin': int(i2c_address)})
            return (cls.SUCCESS_STATUS, json_response)
        else:
            return (cls.FAILURE_STATUS, json_response)
