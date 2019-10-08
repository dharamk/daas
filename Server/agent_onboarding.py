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

import db_firestore_admin
import uuid

EMWEBED_SRV_AGENT_UUID_NAMESPACE = uuid.UUID('2149f591-528e-40e1-84ba-81ee9241d744')


class AgentOnboardingService:
    def __init__(self, db_handle=None):
        if not db_handle:
            self.db = db_firestore_admin.FirestoreAdminClient('dummy')
        else:
            self.db = db_handle

    def lookup_agent_uri(self, ip_address, port=None):
        """
        check if any existing agent is using this ip-address and the port.
        Return True if port is None and ip-address matches or
        both ip-address/port matches.Otherwise, returns False.
        """
        ports_list = []
        ag_list = self.db.get_agent_list(ip_address)
        for ag in ag_list:
            pass
        return False

    def lookup_agent_name(self, agent_name):
        """
        Returns True if the given name is already in use by another agent - else return False
        """
        pass

    def create_new_agent(self, agent_id, agent_name, user_id, ip_address, port):
        """
        the caller should ensure that user is logged in
        and user-id/password combination is valid
        """

    def detach_agent(self, user_id, password, agent_id):
        pass

    def check_uri_in_use(self, ip_addr, port):
        pass

    def get_unique_name(self, name_prefix=None, owner_id='default'):
        """
        User(owner) will either provide a name or won't. If name provided
        by user is unique - allow the name to be used. If not unique, treat it
        as a prefix and suffix it with some auto-generated token to make it unique.
        Also, if user, does not provide a name, generate a longer token and use that
        as a name.
        """
        PREFIX_NAME_LENGTH = 8
        SUFFIX_TOKEN_LENGTH = 6
        name = None
        token = None
        import secrets
        import string

        if not name_prefix:
            prefix = ''.join(secrets.choice(string.ascii_letters) for i in range(PREFIX_NAME_LENGTH))
            suffix = ''.join(secrets.choice(string.digits) for i in range(SUFFIX_TOKEN_LENGTH))
            name = prefix + '_' + suffix
            token = suffix
        else:
            name = name_prefix
            if self.db.has_agent_name(name, owner_id):
                print("Found another agent with same name: {}".format(name))
                suffix = ''.join(secrets.choice(string.digits) for i in range(SUFFIX_TOKEN_LENGTH))
                prefix = name
                name = name + '_' + suffix
            else:
                name = name_prefix
                suffix = None
                prefix = None

        return {"prefix": name_prefix, "name": name, "suffix": suffix}

    def get_unique_agent_id(self, agent_name, owner_id):
        # agent-id are uuid'ed on unique name each agent Must have.
        # Given a name, server will always return same UUID as
        # namespace is fixed.
        if not agent_name or not owner_id:
            raise ValueError

        import uuid
        owner_uuid = uuid.uuid5(EMWEBED_SRV_AGENT_UUID_NAMESPACE, owner_id)
        return uuid.uuid5(owner_uuid, agent_name).hex

    def create_agent(self, aid, name_json, owner_id):
        """
        Commit the new agent information in database
        """
        if not aid or not name_json or not owner_id:
            raise ValueError

        if not self.db:
            raise AttributeError

        if self.db.has_agent_id(aid):
            raise ValueError

        if self.db.has_agent_name(name_json["name"]):
            raise ValueError
        ip_addr = None
        port = None
        self.db.create_new_agent(aid, name_json, owner_id, ip_addr, port)

        return


# def generic_onboard_request(agent_name=None, user_id='default',
#                             ip_address, service, port=None):
#     if not service or not user_id or not ip_address:
#         raise ValueError

    # bare-minimum - we need the server to create a record for the agent
    # including an agent-id, agent-name(automatically generated), tagged user-id,
    # ip-address, port-number being in use


if __name__ == '__main__':
    onboarding = AgentOnboardingService()

    # the user will login first before it can onboard a new agent.
    # hence giving us the owner_id/user_id of this agent
    owner_id = 'default'
    # user should provide 'name' of the agent to uniquely identify
    # all the agents this user has. If the user provides a common name
    # which is already in-use, the server can generate extra suffix and
    # and append with the user-provided name
    # In caes, User does not provide it, A less-readable alpha-numeric name
    # can be generated and passed
    agent_name = 'my-ubuntu-agent'


    # # user may provide a default port or no port at all during onboarding time.
    # # for example - once an agent is created on a web-page,
    # # user may not wish to enter a port number.
    # port = 12121
    # # provide the ip-address of this device - this will get extracted
    # # from network packet headers
    # ip_address = 'localhost'

    name_dict = onboarding.get_unique_name(agent_name, owner_id)
    print(name_dict)
    unique_id = onboarding.get_unique_agent_id(name_dict['name'], owner_id)
    onboarding.create_agent(unique_id, name_dict, owner_id)

    # see the name is duplicate case
    print("--- trying duplicate name case ---")
    agent_name = 'my-ubuntu-agent'
    name_dict = onboarding.get_unique_name(agent_name, owner_id)
    print(name_dict)
    unique_id = onboarding.get_unique_agent_id(name_dict['name'], owner_id)
    onboarding.create_agent(unique_id, name_dict, owner_id)

    # check if name is null
    agent_name = None
    owner_id = 'default'
    name_dict = onboarding.get_unique_name(agent_name, owner_id)
    unique_id = onboarding.get_unique_agent_id(name_dict['name'], owner_id)
    onboarding.create_agent(unique_id, name_dict, owner_id)

    # again... both names should be different
    agent_name = None
    owner_id = 'default'
    name_dict = onboarding.get_unique_name(agent_name, owner_id)
    unique_id = onboarding.get_unique_agent_id(name_dict['name'], owner_id)
    onboarding.create_agent(unique_id, name_dict, owner_id)

