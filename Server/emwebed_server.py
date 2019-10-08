#!/bin/python3
import time

from flask import Flask

from agent_manager import AgentManager
from agent_onboarding import AgentOnboardingService
from db_firestore_admin import FirestoreAdminClient

import server_views as views


class EmwebedServer:
    EMWEBED_SERVER_INSTANCE = None

    @classmethod
    def get_server(cls):
        return cls.EMWEBED_SERVER_INSTANCE

    @classmethod
    def set_server(cls, obj):
        cls.EMWEBED_SERVER_INSTANCE = obj

    @classmethod
    def get_web_app(cls):
        return cls.EMWEBED_SERVER_INSTANCE.web_app

    @classmethod
    def get_db(cls):
        return cls.EMWEBED_SERVER_INSTANCE.db

    @classmethod
    def get_agent_onboarding_service(cls):
        return cls.EMWEBED_SERVER_INSTANCE.agent_onboarding_svc

    def __init__(self, settings=None):

        self.settings = settings

        self.web_app = Flask(__name__)
        views.register_agent_views(self.web_app)
        self.agent_manager = AgentManager()

        self.agent_manager.running = False

        if settings and settings['db'] and settings['db']['root']:
            self.db = FirestoreAdminClient(
                self, root_collection=settings['db']['root'])
        else:
            self.db = FirestoreAdminClient(self)

        self.agent_onboarding_svc = AgentOnboardingService(self.db)

        pass

    def start(self):
        print("[Server] Starting Web Server...")
        # don't do this on deployment !!
        self.web_app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)

    def stop(self):
        pass

if __name__ == '__main__':
    server = EmwebedServer.get_server()
    if not server:
        server = EmwebedServer()
        EmwebedServer.set_server(server)

    d = EmwebedServer.get_db()
    print(d)
    wp = EmwebedServer.get_web_app()
    print(wp)

    server.start()

    while True:
        try:
            time.sleep(1.0)
        except KeyboardInterrupt as e:
            server.stop()
            time.sleep(1.0)
            raise e


# class EmwebedCmdLineServer(EmwebedServer):
#     def __init__(self):
#         pass


# class EmwebedWebServer(EmwebedServer):
#     def __init__(self):
#         pass

