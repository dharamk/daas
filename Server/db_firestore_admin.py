#!/bin/python3
#!/bin/python3
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore

import db_interface


FIRESTORE_DB_TEST_AGENTS_COLLECTION = "testing_agents"
FIRESTORE_DB_PRODUCTION_AGENTS_COLLECTION = "production_agents"

FIRESTORE_DB_ALL_AGENTS_MAIN_DOC = "all_agents"
FIRESTORE_DB_ALL_AGENTS_INFO_DOC = "all_agents_info"
FIRESTORE_DB_ALL_AGENTS_SECURITY_DOC = "all_agents_secure_data"

FIRESTORE_DB_ONLINE_AGENTS_DOC = "online_agents"
FIRESTORE_DB_ONLINE_AGENTS_DATA_COLL = 'data'

FIRESTORE_DB_ALL_DEVICES_MAIN_DOC = "devices"

DEFAULT_SERVICE_ACCOUNT_JSON_NAME = "db_firebase_admin.json"


# Schema of document 'all_agents'
# {
#  "metadata" : {
#       "count": 500,
#       "agent_ids":[]
#   },
# }

ALL_AGENTS_MAIN_METADATA_KEY = 'metadata'
ALL_AGENTS_MAIN_AGENT_IDS = 'metadata.agent_ids'
ALL_AGENTS_MAIN_AGENT_COUNT = 'metadata.count'

ALL_AGENTS_SECURITY_SCHEME = 'security_scheme'
ALL_AGENTS_SECURITY_PRIV_KEY_ID = 'private_key_id'
ALL_AGENTS_SECURITY_PRIV_KEY = 'private_key'

ALL_AGENTS_INFO_AGENT_NAME = 'name'
ALL_AGENTS_INFO_AGENT_OWNER_ID = 'owner_id'
ALL_AGENTS_INFO_AGENT_CREATION_TIMESTAMP = 'created_at'
ALL_AGENTS_INFO_AGENT_SHARED_BY_USERS = "is_shared"

ONLINE_AGENTS_METADATA_KEY = 'metadata'
ONLINE_AGENTS_AGENT_COUNT = 'metadata.count'
ONLINE_AGENTS_AGENT_IDS = 'metadata.agent_ids'
ONLINE_AGENTS_DATA_AGENT_IP_ADDR = 'ip_address'
ONLINE_AGENTS_DATA_AGENT_PORT = 'port'


class FirestoreAdminClient(db_interface.AbstractDbClient):

    def __init__(self, server_obj, root_collection=None, use_test=True):
        """
        initialize and set-up the database client
        """
        self.server = server_obj

        if root_collection:
            self.root_collection = root_collection
        elif not use_test:
            raise ValueError
        else:
            self.root_collection = FIRESTORE_DB_TEST_AGENTS_COLLECTION

        from pathlib import Path
        self.admin_creds = credentials.Certificate(
            str(Path.cwd() / DEFAULT_SERVICE_ACCOUNT_JSON_NAME))

        self.admin_app = firebase_admin.initialize_app(self.admin_creds)

        self.client = firestore.client()
        self.root_collection_ref = self.client.collection(self.root_collection)

        self.all_agents = self.root_collection_ref.document(
            FIRESTORE_DB_ALL_AGENTS_MAIN_DOC)

        self.online_agents = self.root_collection_ref.document(
            FIRESTORE_DB_ONLINE_AGENTS_DOC)

        self.online_agents_data = self.online_agents.collection(
            FIRESTORE_DB_ONLINE_AGENTS_DATA_COLL)
        # self.online_agents_data = self.client.collection(
        #     self.root_collection, FIRESTORE_DB_ONLINE_AGENTS_DOC, FIRESTORE_DB_ONLINE_AGENTS_DATA_COLL)

        self.all_agents_info = self.root_collection_ref.document(
            FIRESTORE_DB_ALL_AGENTS_INFO_DOC)

        # self.root_collection_ref.document.document(FIRESTORE_DB_ALL_AGENTS_SECURITY_DOC)
        self.all_agents_security = self.root_collection_ref.document(
            FIRESTORE_DB_ALL_AGENTS_SECURITY_DOC)

    def _is_agent_id_in_use(self, aid):
        """
        Checks if given Agent-id has already been registered(onboarded)
        with the Server.

        Args:
            aid (str): Agent unique id

        Returns:
            Boolean : True if the agent-id is already registered with Server
            else return False

        """
        if not self.all_agents:
            raise AttributeError
        if not aid:
            raise ValueError

        doc = self.all_agents
        array_agent_ids = doc.get([ALL_AGENTS_MAIN_AGENT_IDS]).get(
            ALL_AGENTS_MAIN_AGENT_IDS)

        if array_agent_ids and aid in array_agent_ids:
            return True

        return False

    def _add_agent_main(self, aid):
        if not aid or not self.all_agents:
            raise ValueError
        doc = self.all_agents

        t = {}
        t['count'] = 1
        t['agent_ids'] = [aid]

        snapshot = doc.get().to_dict()
        if not snapshot:
            doc.set({ALL_AGENTS_MAIN_METADATA_KEY: t})
        else:
            doc.update({ALL_AGENTS_MAIN_AGENT_COUNT: firestore.Increment(1)})
            doc.update(
                {ALL_AGENTS_MAIN_AGENT_IDS: firestore.ArrayUnion([aid])})

    def _add_agent_security(self, aid, security_options=None):
        if not aid or not self.all_agents_security:
            raise ValueError
        doc = self.all_agents_security
        # TODO: enhance this once we figure out what all schemes we've to use
        snapshot = doc.get()
        if not snapshot.to_dict():
            doc.set({aid: {ALL_AGENTS_SECURITY_SCHEME: None}})
        else:
            doc.update({aid: {ALL_AGENTS_SECURITY_SCHEME: None}})

    def _delete_agent_main(self, aid):
        if not aid or not self.all_agents:
            raise ValueError

        doc = self.all_agents
        snapshot = doc.get()
        print(snapshot.to_dict())
        if not snapshot.to_dict():
            print("agent_main: Document empty. aid:{}".format(aid))
            return

        array_ids = snapshot.get(ALL_AGENTS_MAIN_AGENT_IDS)
        print(array_ids)
        if array_ids and aid in array_ids:
            doc.update({ALL_AGENTS_MAIN_AGENT_COUNT: firestore.Increment(-1)})
            doc.update(
                {ALL_AGENTS_MAIN_AGENT_IDS: firestore.ArrayRemove([aid])})
        else:
            print("Agent-id not found")

    def _delete_agent_security(self, aid):
        if not aid or not self.all_agents_security:
            raise ValueError

        doc = self.all_agents_security
        snapshot = doc.get()
        print(snapshot.to_dict())
        if not snapshot.to_dict():
            print("agent_security: Document empty. aid:{}".format(aid))
            return
        # agent_security = snapshot.
        # print(agent_security)
        doc.update({aid: firestore.DELETE_FIELD})

        pass

    def _add_agent_info(self, aid, name, uid, is_shared=True):
        if not aid or not name or not uid:
            raise ValueError

        coll = self.all_agents_info.collection('data')
        agent_doc = coll.document(aid)

        t = {}
        t[ALL_AGENTS_INFO_AGENT_NAME] = name
        t[ALL_AGENTS_INFO_AGENT_CREATION_TIMESTAMP] = firestore.SERVER_TIMESTAMP
        t[ALL_AGENTS_INFO_AGENT_SHARED_BY_USERS] = is_shared
        t[ALL_AGENTS_INFO_AGENT_OWNER_ID] = uid

        # this method should reset the full document.
        # ideally this would be called once by the Server at very beginning.
        agent_doc.set(t)

    def _delete_agent_info(self, aid):
        if not aid:
            raise ValueError

        coll = self.all_agents_info.collection('data')
        agent_doc = coll.document(aid).delete()

    def _add_agent_connection(self, aid, ip_addr, port):
        if not aid:
            raise ValueError

        pdoc = self.online_agents
        psnapshot = pdoc.get()

        if not psnapshot.to_dict():
            t = {}
            t['count'] = 0
            t['agent_ids'] = []
            print("yes-parent-doc is empty")
            pdoc.set({ONLINE_AGENTS_METADATA_KEY: t})
        else:
            # do-nothing if a new agent-connection info is received
            # agent will update the 'connection-status' i.e. its live status
            # once the agent-service is online. This function is called
            # very first time the agent is created(and not ONLINE).
            # so these fields will be udpated in a different flow.
            pass

        ag = {}
        ag[ONLINE_AGENTS_DATA_AGENT_PORT] = port
        ag[ONLINE_AGENTS_DATA_AGENT_IP_ADDR] = ip_addr

        child_collection = self.online_agents_data
        doc = child_collection.document(aid)
        doc.set(ag)
        pass

    def _delete_agent_connection(self, aid):
        if not aid:
            raise ValueError
        parent_doc = self.online_agents
        p_snapshot = parent_doc.get()
        if p_snapshot.to_dict():
            online_agents = p_snapshot.get(ONLINE_AGENTS_AGENT_IDS)
            if online_agents and aid in online_agents:
                parent_doc.update(
                    {ONLINE_AGENTS_AGENT_IDS: firestore.ArrayRemove([aid])})
                parent_doc.update(
                    {ONLINE_AGENTS_AGENT_COUNT: firestore.Increment(-1)})
            else:
                # do nothing if there is no live-information about this agent
                # with server.
                pass

        doc = self.online_agents_data.document(aid)
        snapshot = doc.get()
        print(snapshot.to_dict())
        if not snapshot.to_dict():
            # .document(aid) creates the document by default if it does not exist.
            # if it has been deleted in the past we have inadvertently created it
            # so just-delete it - i.e. no return from this if-check
            print("agent_connection: Document empty. aid:{}".format(aid))
        self.online_agents_data.document(aid).delete()

        pass

    def _get_agent_by_name(self, name_args, owner_id='default'):
        if not name_args:
            return None

        full_name = None

        if isinstance(name_args, dict):
            # name_prefix = name_json['prefix']
            # name_token = name_json['token']
            full_name = name_args['name']
        elif isinstance(name_args, str):
            full_name = name_args

        coll = self.all_agents_info.collection('data')
        docs = coll.where('name.name', '==', full_name).where(
            'owner_id', '==', owner_id).stream()
        count = 0
        t = None
        if docs:
            for doc in docs:
                if count == 1:
                    # if we ever have two documents(agents) with same full-name
                    # it would be a disaster - so report it.
                    raise ValueError
                count += 1
                # print(doc.get().to_dict())
                t = dict()
                t["aid"] = doc.id
        return t

    def _get_agent_by_id(self):
        pass

    def _get_agent_by_uri(self, ip_addr, port):
        """
        Gets the list of Agent(s) matching with given ip-address and port.
        There MUST be only one Agent with a given ip-address and port.
        If port is null - return all the agents(list of agent-ids)
        with given ip-address.
        """
        if not ip_addr:
            raise ValueError
        coll = self.online_agents_data
        ip_docs = coll.where('ip_address', '==', ip_addr)
        if not ip_docs:
            return None
        t = None
        # if port is not given, just fetch a list of all
        # the agents with this IP-Address
        if not port:
            agents_list = list()
            for doc in ip_docs.stream():
                agents_list.append(doc.id)
            t = dict()
            t['aid'] = agents_list
            return t

        port_docs = ip_docs.where('port', '==', port).stream()
        count = 0
        if port:
            if port_docs:
                for doc in port_docs:
                    if count == 1:
                        # if we ever have two agents using same ip-address
                        # and same port then raise an exception.
                        raise ValueError
                    count += 1
                    t = dict()
                    t["aid"] = [doc.id]
            return t

    # Public Methods on Database class

    def create_new_agent(self, aid, name, owner_id='default', ip_addr=None, port=None):
        if not name or not aid:
            raise ValueError
        if self._is_agent_id_in_use(aid):
            print("hello- agent is already available")
            raise ValueError

        self._add_agent_main(aid)
        self._add_agent_security(aid)
        self._add_agent_info(aid, name, owner_id)
        self._add_agent_connection(aid, ip_addr, port)

        pass

    def delete_agent(self, aid):
        if not aid:
            raise ValueError

        self._delete_agent_main(aid)
        self._delete_agent_security(aid)
        self._delete_agent_info(aid)
        self._delete_agent_connection(aid)
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

    def get_agent(self, **kargs):
        # 'name'=<some-agent-name>
        # 'aid'=<some-agent-id>
        # 'ip_address'=<some-ip-address>

        pass

    def get_agent_connection_info(self, agent_id):
        if not agent_id:
            raise ValueError

        agent_doc = self.online_agents_data.document(agent_id)
        snapshot = agent_doc.get(['ip_address', 'port'])
        return snapshot.to_dict()

    def has_agent_id(self, aid):
        return self._is_agent_id_in_use(aid)

    def has_agent_name(self, agent_name, owner_id='default'):
        if not agent_name:
            raise ValueError

        d = self._get_agent_by_name(agent_name, owner_id)
        if not d:
            print("agent by Name not found {}".format(agent_name))
            return False

        return True

    def has_agent_ip_addr_and_port(self, ip_addr, port):
        if not ip_addr:
            raise ValueError

        d = self._get_agent_by_uri(ip_addr, port)
        if not d:
            return False
        return True

    def get_agent_by_ipaddr_and_port(self, ip_addr, port):
        if not ip_addr:
            raise ValueError

        d = self._get_agent_by_uri(ip_addr, port)
        return d

    def set_agent_ipaddr_port(self, aid, ip_addr, port):
        if not aid:
            raise ValueError

        agent_doc = self.online_agents_data.document(aid)

        agent_doc.update({
            'ip_address': ip_addr,
            'port': port,
        })

    def verify_token(self, token_id, current_user=None):
        if not token_id or not current_user:
            raise ValueError
        try:
            decoded_token = auth.verify_id_token(token_id, check_revoked=True)
            uid = decoded_token['uid']
            if current_user:
                if uid is not current_user:
                    raise ValueError
        except auth.RevokedIdTokenError:
            # Token revoked, inform the user to reauthenticate or signOut()
            # return status and whether it needs to sign-in again
            return (False, True)

        except auth.InvalidIdTokenError:
            # Token is invalid
            return {False, False}

        return (True, False)

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
        for key, value in kwargs.items():
            pass

    def find_agent_by_ip_address(self, ip_address, port):
        if not ip_address:
            raise ValueError

        all_agents = self.agents.collections().where('ip-address', '==', ip_address)
        pass




def test_create_delete_agents(db):
    db.create_new_agent("12567", "agent-name-12567",
                        "default", "192.168.1.15", 12121)
    db.create_new_agent("12568", "agent-name-12568",
                        "default", "192.168.1.16", 12122)
    db.delete_agent("12569")
    # print(db._get_agent_by_name("agent-name-12568").to_dict())
    t = db._get_agent_by_name("agent-name-12568")
    print("agent-details for id: {} => {}".format("agent-name-12568", t))

    t = db._get_agent_by_name("agent-name-12569")
    print("agent-details for id: {} => {}".format("agent-name-12569", t))

    t = db._get_agent_by_name("agent-name-12567")
    print("agent-details for id: {} => {}".format("agent-name-12567", t))
    # db.delete_agent("12567")
    # db.delete_agent("12568")
    # db.delete_agent("12568")


if __name__ == '__main__':

    agent_obj = 'dummy'
    db = FirestoreAdminClient(
        agent_obj, root_collection="foo_testing")

    db.create_new_agent(
        "asdfaksdfkasdf", "agent-name-asdfad12567", "default", "192.168.1.15", 12121)
    # test_create_delete_agents(db)

    # db.create_new_agent("12569", "agent-name-12569", "default", "192.168.1.17", 12121)

    # agent_dict = {"aid": "123456",
    #               "name": "agent-dummy-name-1", "host": "ubuntu"}
    # gcp_db.update_agent(agent_dict["aid"], agent_dict)

    # agent_dict = {"aid": "123455",
    #               "name": "agent-dummy-name-2", "host": "ubuntu"}
    # gcp_db.update_agent(agent_dict["aid"], agent_dict)

    # agent_dict = {"aid": "123458",
    #               "name": "agent-dummy-name-3", "host": "ubuntu"}
    # gcp_db.update_agent(agent_dict["aid"], agent_dict)
