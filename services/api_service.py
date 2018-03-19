import requests
from config.config import CONFIG


class ApiService:
    """
    This class will be responsible for communicating with our Heroku hosted API to create and update existing desks
    """

    BASE_URL = CONFIG.debug_config.api_base

    @classmethod
    def create_desk(cls, name):
        """
        :param name: Name of desk to be created
        :return: Response object
        """
        return cls.__notify('post', '/desks.json', {'desk': {'name': name}})

    @classmethod
    def update_desk_occupied_status(cls, desk_id, occupied_status):
        """
        :param id: ID of desk
        :param occupied_status: New occupied status of desk

        :return: Response object
        """

        return cls.__notify('put', f'/desks/{desk_id}.json', {'desk': {'occupied': occupied_status}})

    @classmethod
    def __notify(cls, method, endpoint, payload=None):
        """
        Calls cloud API with specified method and payload

        :param method: HTTP method, i.e 'get', 'post', 'put'
        :param endpoint: Relative endpoint to BASE URL
        :param payload: Data to be sent in request body

        :return: Response
        """
        return requests.request(method, cls.BASE_URL + endpoint, headers={'Content-Type': 'application/json'}, json=payload)
