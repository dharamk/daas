#!/bin/python3

class DaaSServer:
    DAAS_SERVER_INSTANCE = None

    @classmethod
    def get_daas_server(cls):
        return cls.DAAS_SERVER_INSTANCE

    @classmethod
    def set_daas_server(cls, obj):
        cls.DAAS_SERVER_INSTANCE = obj

    def __init__(self):
        pass


class DaasCmdLineServer(DaaSServer):
    def __init__(self):
        pass


class DaaSWebServer(DaaSServer):
    def __init__(self):
        pass

