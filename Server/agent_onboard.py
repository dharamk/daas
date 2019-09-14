#!/bin/python3

"""
A new Agent is trying to host the device. Agent could be internally-hosted(local network)
or in cloud(remote). Before an Agent can host the device - it has to register its identity
and authenticate itself with Server. One can imagine different scenarios/flows where an Agent
is getting deployed.

#1 - User goes to website. Chooses to 'host a device' option. The server prompts
     the user to download a Tool/Software to achieve it. The software/tool comes pre-loaded
     with necessary configuration/tokens etc. for the tool to access the Server(and its database if required).
     The Agent can issue a read/write to database about its ever-changing device information/configuration etc.

#2 - Admin deploys the script to install and run multiple agents(different host machines).
     The agents will pick up a common configuration to access the server.


##Requirements##
i.   Each Agent instance has to be tied to an user-id/email/password.
ii.  A user can have one or more agent instances running from different hosts.
iii. An Agent Instance can only run from one Host machine. Duplicating of Agent instances is not allowed.
iv.  Each Agent Instance(once onboarded) gets an unique Agent-ID.
v.   Server owns and stores Secret-keys associated with each agent-instance(agent-id)
vi.  Server issues Tokens(JWTs for example) to each Agent Instance(i.e. tied with Agent-ID)
"""

"""
agent_client.connect(server)
agent_id, jwt_token = agent_client.onboard()
devs = agent_client.scan_devices()
"""

import db_firestore


class ServerAgentOnboardingService:
    def __init__(self, db_handle=None):
        if not db_handle:
            self.db = db_firestore.FirestoreDbClient()
        else:
            self.db = db_handle

    def attach_new_agent(user_id, password, agent_id=None):
        try:
            if self.db.check_user_password(user_id, password):
                pass
        except Exception as e:
            raise e

    def detach_agent(user_id, password, agent_id):
        pass

