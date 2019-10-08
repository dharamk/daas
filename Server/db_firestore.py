#!/bin/python3

import db_interface
from google.cloud import firestore

FIRESTORE_DB_TEST_AGENTS_COLLECTION = "testing_agents"
FIRESTORE_DB_PRODUCTION_AGENTS_COLLECTION = "production_agents"


#
#(coll)testing_agents
#
#(document)all-agents
# {
#  "metadata" : {
#       "count": 500,
#       "all-agent-ids":[]
#   },
# }
#
#(document)online-agents
# {
#     "metadata": {
#         "agents-count": 5,
#         "agents-id-list": [],
#     },
#     "data" :{
#         "agent-id-1": {
#             "ip-address": "agent-current-ip-address",
#             "port" : <agent-current-port-number>,
#             "user-id": "<current-user-crednetials/id/email in-use>",
#             "grpc_running": "running/stopped/suspended",
#             "scanner_running": "running/stopped/suspended",
#             "devices": {
#                 "detected": ['device-id-0', 'device-id-1',
#                              'device-id-2', 'device-id-4'],
#                 "busy": ['device-id-0', 'device-id-4'],
#             },
#         },
#         "agent-id-2" :{
#             "ip-address": "agent-current-ip-address",
#             "port" : <agent-current-port-number>,
#             "user-id": "<current-user-crednetials/id/email in-use>",
#             "grpc_running": "running/stopped/suspended",
#             "scanner_running": "running/stopped/suspended",
#             "devices": {
#                 "detected": ['device-id1-0', 'device-id1-4',
#                             'device-id1-3', 'device-id1-5'],
#                 "busy": ['device-id1-0', 'device-id1-4'],
#             },
#         },
#         ... # other online agents details follow from here
#     },
# }
#
#
#
#
# (document) all-agent-security-data
# {
#     "metadata": {
#     # keep some metadata information about security-aspects related to agents.
#     # note that this collection MUST be accessible to Admin/Server only.
#     },
#
#     "agent-id-1": {
#         # identifies what kind of security scheme the agent is configured with
#         "security_scheme": "private-key or jwt or default or none"
#         # another table which is storing all private-keys generated - should be None if not in use"
#         "private_key_id": "private-key-index to fetch private-key if generated"
#     },
#
#     "agent-id-2": {
#      ...
#     },
# },


FIRESTORE_DB_AGENTS_TOP_DOCUMENT = "agents"
FIRESTORE_DB_DEVICES_TOP_DOCUMENT = "devices"

DEFAULT_SERVICE_ACCOUNT_JSON_NAME = "agent_firebase_admin.json"


class FirestoreDbClient(db_interface.AbstractDbClient):

    def __init__(self):
        """
        initialize and set-up the Firestore Database Client.
        it will first look for GOOGLE_APPLICATION_CREDENTIALS path to be set.
        if it is already set - it will reuse the configuration.
        Else - it will try to look for 'db_firestore.json' file in
        current-directory. If not found, it will raise an exception.
        If found, it will set the environment variable setting.
        """
        import os
        from pathlib import Path

        DEFAULT_GCP_APP_ENVIRON_KEY = "GOOGLE_APPLICATION_CREDENTIALS"
        DEFAULT_GCP_APP_CONFIG_NAME = "db_firestore.json"

        gcp_environ_found = os.environ.get(DEFAULT_GCP_APP_ENVIRON_KEY)
        if not gcp_environ_found:
            print("Google Application Credential not found - trying for {}...".format(
                DEFAULT_GCP_APP_CONFIG_NAME))
            try:
                f = open(DEFAULT_GCP_APP_CONFIG_NAME)

                f.close()
                os.environ[DEFAULT_GCP_APP_ENVIRON_KEY] = str(
                    Path.cwd() / DEFAULT_GCP_APP_CONFIG_NAME)
            except IOError:
                print("Could not find {} either.".format(
                    DEFAULT_GCP_APP_CONFIG_NAME))
                raise IOError

        self.db = firestore.Client()
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

    def find_agent(self, agent_id, collection=None):
        """
        returns a dictionary corresponding to agent_id document
        """
        if not agent_id:
            raise ValueError

        if not collection:
            agents_ref = self.db.collection(u'test/agents')
        else:
            agents_ref = self.db.collection(collection)

        agents_ref.document(agent_id)
        pass

    def find_agent_by_ip_address(self, ip_address, collection_id=None):
        collection = self.db.collection('testing_ag')
        agents_ref = self.db.collection('testing/agents')

        pass

    def find_agent_by_name(self, agent_name):
        pass

    def find_device_by_name(self, device_name):
        pass

    def get_user(self, user_id):
        """
        get the document matching to the user-id from 'users' collection
        """
        pass

    def check_user_password(self, user_id, passcode):
        """
        check if the existing user-id/passcode exists and matches
        """
        return False

    def write_test(self, data=None, collection=None, document=None):
        doc_ref = self.db.collection(u'users').document(u'aturing')
        if data:
            doc_ref.set(data)
        else:
            doc_ref.set({
                u'first': u'Alan',
                u'middle': u'Mathison',
                u'last': u'Turing',
                u'born': 1912
            })
        pass

    def read_test(self, collection=None, document=None):
        users_ref = self.db.collection(u'users')
        docs = users_ref.stream()

        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

        pass


if __name__ == '__main__':
    firestore_db = FirestoreDbClient()
    firestore_db.write_test(
        {u'first': u'Dharam', u'last': u'kumar', u'born': 1987})
    firestore_db.read_test()
