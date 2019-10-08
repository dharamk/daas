#!/bin/python3

import abc

class AgentDBService(metaclass=abc.ABCMeta):
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

    def update_device_status(self, device_id):
        pass

    def update_agent_status(self, agent_dict):
        pass


class AgentDocument:
    def __init__(self, agent_instance):
        if not agent_instance:
            raise ValueError
        self.agent_dict = {}
        self.agent_dict["aid"] = agent_instance.host_id
        self.agent_dict["name"] = agent_instance.name
        self.agent_dict["ip-address"] = agent_instance.address
        self.agent_dict["port"] = agent_instance.server_port
        self.agent_dict["user-id"] = None
        self.agent_dict["status"] = "offline"
        self.agent_dict["grpc-server-started"] = agent_instance.server_started
        self.agent_dict["device-scanner-started"] = agent_instance.scanner_started
        devs = dict()

        self.agent_dict["devices"] = devs

        devs["detected"] = agent_instance.get_device_list()
        for dev_id in devs["detected"]:
            dev_obj = agent_instance.get_device(dev_id)
            dev_summary = dict()
            devs[dev_id] = dev_summary
            dev_summary["name"] = dev_obj.get_name()
            dev_summary["device-type"] = dev_obj.get_type()
            dev_summary["status"] = dev_obj.get_status()



# SERVICE_ACCOUNT_KEY_PATH2="/home/dkumar/firebase-example-252109-firebase-adminsdk-r8cgl-8297fc9621.json"

# cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH2)
# default_app = firebase_admin.initialize_app(cred)


# email="zoo@xyz.com"
# user = auth.get_user_by_email(email)
# print('Successfully fetched user data: {0}'.format(user.uid))
# foo_user = auth.update_user(uid=user.uid,password="secret_password")
# print('Sucessfully updated user: {0}'.format(foo_user.uid))

# email="foo@xyz.com"
# user = auth.get_user_by_email(email)
# print('Successfully fetched user data: {0}'.format(user.uid))

# uid = 'some-uid'
# custom_token = auth.create_custom_token(uid)
# print(custom_token)

# print(default_app.name)

