#!/bin/python3
import abc

class AbstractDbClient(metaclass=abc.ABCMeta):

    def __init__(self):
        """
        initialize and set-up the database client
        """
        pass

    def connect(self):
        """
        connects to Database Server
        """
        pass

    def disconnect(self):
        """
        disconnects to Database server
        """
        pass

    def find_device(self, device_id):
        pass

    def find_agent(self, agent_id):
        pass

    def find_agent_by_name(self, agent_name):
        pass

    def find_device_by_name(self, device_name):
        pass

