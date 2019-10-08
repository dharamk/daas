#!/bin/python3

from flask import Flask, abort, request, Blueprint, render_template

from emwebed_server import EmwebedServer

from agent_onboarding import AgentOnboardingService

# app = Flask(__name__)
# agent_endpoints = Blueprint('agent_endpoints', __name__, url_prefix='/agent')
# app.register_blueprint(agent_endpoints)


# @app.route('/user/create_agent', methods=['POST'])
def index():
    return render_template('main.html')

def create_agent():
    json_body = request.json
    if not json_body:
        abort(400)
    if not json_body['idToken']:
        abort(401)

    token = json_body['idToken']
    db = EmwebedServer.get_db()
    db.verify_token(token)
    onboarder = EmwebedServer.get_agent_onboarding_service()

    pass


# @agent_endpoints.route('/user/login', methods=['POST', 'GET'])
# @app.route('/agent/user/login', methods=['POST', 'GET'])
def do_agent_login():
    json_body = request.json
    if not json_body:
        abort(400)
    if not json_body['idToken']:
        abort(401)

    token_id = json_body['idToken']

    db = EmwebedServer.get_db()



    # verify the user details using this token
    pass

# @agent_endpoints.route('/user/logout', methods=['POST', 'GET'])
# @app.route('/agent/user/logout', methods=['POST', 'GET'])
def do_agent_logout():
    return "logging out"
    pass



# @app.route('/verifyAgent', methods=['GET'])
def do_agent_verification():
    """
    {
        "agent_id":
        "agent_name":
        "created-at":
        "is-shared":
    }
    """
    return "hello world"
    pass

# @agent_endpoints.route('/user/signup', methods=['POST'])
# @app.route('/agent/user/signup', methods=['POST'])
def do_agent_signup():
    pass


# @agent_endpoints.route('/status/<type>', methods=['POST'])
# @app.route('/agent/status/<status_type>', methods=['POST'])
def update_agent_status():

    json_body = request.json
    if not json_body:
        abort(400)

    token_id = json_body['idToken']
    agent_id = json_body['aid']

    db = EmwebedServer.get_db()

    if not db:
        abort(500)

    if not token_id:
        abort(401)

    if not agent_id or not db.has_agent_id(agent_id):
        abort(400)

    # TODO Access check based on idtoken - return forbidden(403)
    # the given token is not allowed with this agent.

    # ensure that no agent is using same ip-address and port
    if status_type == 'connection':
        ip_address = json_body['ip_address']
        grpc_port = json_body['grpc_port']
        if ip_address and grpc_port:
            current_agent = db.get_agent_by_ipaddr_and_port(ip_address, grpc_port)
            if current_agent['aid'] != agent_id:
                abort(409)  # could not be completed because of a conflict

        db.set_agent_ipaddr_port(agent_id, ip_address, grpc_port)


# @agent_endpoints.route('/info', methods=['POST', 'GET'])
# @app.route('/agent/info', methods=['POST', 'GET'])
def ag_info_handler():
    """
    {
      "user_id_token": "<Token-ID of current logged-in User>",
      "agent_id": "the agent-id for which this post/get request is for",
    }
    """
    # get database service instance
    db = EmwebedServer.get_db()

    json_body = request.json
    user_id_token = json_body['user_id_token']
    agent_id = json_body['agent_id']

    if not agent_id or not user_id_token:
        abort(401)
    if request.method == 'POST':
        # 1. verify the user_id_token using firebase_admin APIs
        # 2. get the user details

        # decoded_token = auth.verify_id_token(user_id_token)
        # uid = decoded_token['uid']
        uid = None
        # user = auth.get_user(uid)

        # this agent-id has never been registered with the server
        if not db.has_agent_id(agent_id):
            abort(401)

        # if this logged-in user can change the agent_id public information
        if db.check_access(agent_id, user_id_token):
            pass

        # agent wants to update some meta-information about it
        # for example - port-number, ip-address in use etc.
    elif request.method == 'GET':
        # agent wants to get some basic information about it
        pass

    pass


# @agent_endpoints.route('/connect/<agent_id>', methods=['PUT'])
# @app.route('/agent/connect', methods=['PUT'])
def ag_connect_handler():
    pass


# @agent_endpoints.route('/disconnect/<agent_id>', methods=['PUT'])
# @app.route('/agent/disconnect', methods=['PUT'])
def ag_disconnect_handler():
    pass


# sign-in/sign-up login page
def do_user_login():
    return render_template('login.html')


def register_agent_views(app):
    app.add_url_rule('/', 'index', index, methods=['GET'])

    app.add_url_rule('/userlogin', 'user_login',
                     do_user_login, methods=['GET'])

    app.add_url_rule('/verifyAgent', 'do_agent_verification',
                     do_agent_verification, methods=['GET'])

    app.add_url_rule('/agent/user/login', 'ag_login_handler',
                     do_agent_login, methods=['POST', 'GET'])

    app.add_url_rule('/agent/user/logout', 'ag_logout_handler',
                     do_agent_logout, methods=['POST', 'GET'])

    app.add_url_rule('/agent/user/signup', 'ag_signup_handler',
                     do_agent_login, methods=['POST', 'GET'])

    app.add_url_rule('/agent/status/<info>', 'ag_status_handler',
                     update_agent_status, methods=['POST', 'GET'])

    app.add_url_rule('/agent/info', 'ag_info_handler',
                     ag_info_handler, methods=['POST', 'GET'])


# All Agent endpoints must go-through a stringent User-id/Agent-id/
# Access rules.
def auth_verify_access(agent_id, current_user_id):
    pass

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000, Debug=True)
