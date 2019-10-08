#!/bin/python3
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore
# from google.cloud import firestore

import agent_dbservice_base

FIRESTORE_TEST_DB_NAME = "testing"
FIRESTORE_PRODUCTION_DB_NAME = "production"
FIRESTORE_AGENT_COLLECTION_NAME = "agents"
FIRESTORE_DEVICES_COLLECTION_NAME = "devices"
DEFAULT_SERVICE_ACCOUNT_JSON_NAME = "agent_firebase_admin.json"


class AgentDBServiceFirestoreAdminPrivilege(agent_dbservice_base.AgentDBService):

    def __init__(self, agent_obj=None, use_db=None, use_test_db=True):
        """
        initialize and set-up the database client
        """
        self.agent = agent_obj

        if use_db:
            self.db_in_use = use_db
        elif not use_test_db:
            raise ValueError
        else:
            self.db_in_use = FIRESTORE_TEST_DB_NAME

        from pathlib import Path
        self.admin_creds = credentials.Certificate(str(Path.cwd() / DEFAULT_SERVICE_ACCOUNT_JSON_NAME))

        self.admin_app = firebase_admin.initialize_app(self.admin_creds)
        self.agent_instance = agent_obj

        self.db = firestore.client()
        # testing/"agents"/agent_id/
        self.agents = self.db.collection(self.db_in_use).document('agents')
        self.devices = self.db.collection(self.db_in_use).document('devices')
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

    def update_device_status(self, device_id, device_dict=None, detected=False):
        pass

    def update_agent(self, agent_id, agent_dict):
        sub_coll = self.agents.collection(agent_dict["aid"])
        doc = sub_coll.document(agent_dict["aid"]).set(agent_dict)
        pass

    def update_agent_fields(self, agent_id, **kwargs):
        if not agent_id:
            raise ValueError
        sub_coll = self.agents.collection(agent_id)
        doc = sub_coll.document(agent_id)
        for key,value in kwargs.items():
            pass


if __name__ == '__main__':

    agent_obj = 'dummy'
    gcp_db =  AgentDBServiceFirestoreAdminPrivilege(agent_obj)
    agent_dict = {"aid": "123456", "name": "agent-dummy-name-1", "host": "ubuntu"}
    gcp_db.update_agent(agent_dict["aid"], agent_dict)

    agent_dict = {"aid": "123455", "name": "agent-dummy-name-2", "host": "ubuntu"}
    gcp_db.update_agent(agent_dict["aid"], agent_dict)


    agent_dict = {"aid": "123458", "name": "agent-dummy-name-3", "host": "ubuntu"}
    gcp_db.update_agent(agent_dict["aid"], agent_dict)