#!/bin/python3

from flask import abort, request, render_template
from flask import make_response, redirect, url_for, jsonify

from emwebed_server import EmwebedServer

from agent_onboarding import AgentOnboardingService

# app = Flask(__name__)
# agent_endpoints = Blueprint('agent_endpoints', __name__, url_prefix='/agent')
# app.register_blueprint(agent_endpoints)


# @app.route('/user/create_agent', methods=['POST'])

def verify_token_or_redirect(idToken):

    if result['status'] == 'success':
        # return status and whether it needs to sign-in again
        return (True)
    else:
        return (False, True)


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
    onboarder = EmwebedServer.get_agent_onboarding_service()
    success, reauth = db.verify_token(token)
    if success:
        # redirect to 'create_agent.html' page and let user enter Agent-details
        # return render_template('create_agent_form.html')
        pass
    else:
        if reauth:
            # tell user to sign-out and reauthenticate
            # return render_template('notify_user_idtoken_signout.html')
            pass
        # otherwise - invalid token
        abort(401)
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


# @agent_endpoints.route('/info', methods=['POST', 'GET'])
# @app.route('/agent/info', methods=['POST', 'GET'])
def ag_status_handler():
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


def _emwebed_verify_token(token_id, user_id=None):
    if not token_id:
        raise ValueError("Invalid token id provided")

    db = EmwebedServer.get_db()
    if not db:
        raise ValueError("Db Client not defined")

    return db.verify_token(token_id)


def _emwebed_verify_agent(aid):
    """
    Validates whether the given Agent-ID is valid
    """
    return True


def _emwebed_verify_agentuser(aid, uid):
    """
    Validates whether the given user has access this Agent-ID or not.
    Also - If any other user has signed-in to same agent right now.
    """
    return True


# @agent_endpoints.route('/user/login', methods=['POST', 'GET'])
# @app.route('/agent/user/login', methods=['POST', 'GET'])
def signin_agent():

    json_body = request.json
    if not json_body:
        abort(400)
    if not json_body['idToken']:
        abort(401)

    token_id = json_body['idToken']
    user_id = json_body['uid']
    agent = json_body['agent']

    message = dict()
    http_code = 400

    success, reauth = _emwebed_verify_token(token_id, user_id)
    if success:
        message['signin_status'] = 'success'
        http_code = 200
    else:
        if reauth:
            # tell user to sign-out and reauthenticate
            # return render_template('notify_user_idtoken_signout.html')
            message['signin_status'] = 'reauthenication required'
            http_code = 401

        # otherwise - invalid token
        message['signin_status'] = 'Invalid Token'
        http_code = 401


    if http_code != 200:
        return make_response(jsonify(message), http_code)
    # TODO  Check if this
    success = _emwebed_verify_agent(agent['aid'])
    if not success:
        http_code = 400
        message['agent_status'] = 'Invalid Agent Settings'
        return make_response(jsonify(message), http_code)
    success = _emwebed_verify_agentuser(agent['aid'], user_id)
    if not success:
        http_code = 400
        message['agent_status'] = 'Invalid access by User'
        return make_response(jsonify(message), http_code)

    _emwebed_update_agent_current_user()


# @agent_endpoints.route('/user/logout', methods=['POST', 'GET'])
# @app.route('/agent/user/logout', methods=['POST', 'GET'])
def signout_agent():
    json_body = request.json
    if not json_body:
        abort(400)
    if not json_body['idToken']:
        abort(401)

    message = dict()
    message['signout_status'] = 'success'
    return make_response(jsonify(message), 200)


def verify_agent_token():
    json_body = request.json
    if not json_body:
        abort(400)
    if not json_body['idToken'] or not json_body['uid']:
        abort(401)

    message = dict()
    http_code = 400
    token_id = json_body['idToken']
    user_id = json_body['uid']

    success, reauth = _emwebed_verify_token(token_id, user_id)
    if success:
        message['token_status'] = 'valid'
        http_code = 200
    else:
        if reauth:
            # tell user to sign-out and reauthenticate
            # return render_template('notify_user_idtoken_signout.html')
            message['token_status'] = 'revoked'
            http_code = 401

        # otherwise - invalid token
        message['token_status'] = 'Invalid Token'
        http_code = 401
    # render html for login response as well
    return make_response(jsonify(message), http_code)


# @agent_endpoints.route('/status/<type>', methods=['POST'])
# @app.route('/agent/status/<command_type>', methods=['POST'])
def agent_status_handler():
    json_body = request.json
    if not json_body:
        abort(400)

    token_id = json_body['idToken']
    agent_id = json_body['aid']

    db = EmwebedServer.get_db()

    if not db:
        abort(500)

    if not token_id:
        abort(401, "Missing Token-ID")

    if not agent_id or not db.has_agent_id(agent_id):
        abort(400, "Missing Agent-ID or Unknown Agent-ID")

    # TODO Access check based on idtoken - return forbidden(403)
    # the given token is not allowed with this agent.

    # ensure that no agent is using same ip-address and port
    if command_type == 'connection':
        ip_address = json_body['ip_address']
        grpc_port = json_body['grpc_port']
        if ip_address and grpc_port:
            current_agent = db.get_agent_by_ipaddr_and_port(
                ip_address, grpc_port)
            if current_agent['aid'] != agent_id:
                # could not be completed because of a conflict
                abort(409, "Endpoint is already in Use")

        db.set_agent_ipaddr_port(agent_id, ip_address, grpc_port)
        # request.method == 'GET'

    elif command_type == 'service':
        pass
    elif command_type == 'devicelist':
        pass
    elif command_type == 'deviceinfo':
        pass

# ####  User views  ####
def on_user_signin_with_token_id():

    json_body = request.json
    if not json_body:
        abort(400)

    token_id = json_body['idToken']

    db = EmwebedServer.get_db()

    if not db:
        abort(500, "Server Error")

    if not token_id:
        abort(401, "Token-ID was not found in Request body")

    message = dict()
    http_code = 400

    success, reauth = _emwebed_verify_token()

    if success:
        message['status'] = 'success'
        http_code = 200
    else:
        if reauth:
            # tell user to sign-out and reauthenticate
            # return render_template('notify_user_idtoken_signout.html')
            message['status'] = 'reauthenication required'
            http_code = 401

        # otherwise - invalid token
        message['status'] = 'Invalid Token'
        http_code = 401
    # render html for login response as well
    return make_response(jsonify(message), http_code)


def on_user_signup():
    return {}


def on_user_signout():
    return {}


# sign-in/sign-up login page
def do_user_login():
    return render_template('login.html')


def submit_login():
    return redirect(url_for('index'))


def user_auth_views(app):
    # user will be presented a 'sign-in' button on home/welcome page.
    # Once Button is clicked, the Client-side javascript should present a
    # User-login-Form/Modal for user to fill-in. Upon clicking the submit
    # button of that modal page/login-form, the client will establish
    # connection with the Firebase Auth Server...validate the User,
    # fetch the user-details, idToken and then connect it to Emwebed Server
    # with the given id-token.
    # Emwebed Server - using Firebase Admin SDK will validate the idToken
    # if idToken is valid - it will pass a json response "status": "success" with 200
    # if idToken has expired - it should signal the user to re-authenticate
    # itself with firebase-Auth
    #
    app.add_url_rule('/auth/signin', 'auth_user_signin',
                     on_user_signin_with_token_id, methods=['POST'])

    app.add_url_rule('/auth/signup', 'auth_user_signup',
                     on_user_signup, methods=['POST'])

    app.add_url_rule('/auth/signout', 'auth_user_signout',
                     on_user_signout, methods=['POST'])


def agent_views(app):
    """
    Set of views for Agent interaction(Python Emwebed Agents)
    """

    # Allow Agent to log-in without rendering HTML templates
    app.add_url_rule('/agent/auth/signin', 'ag_signin_handler',
                     signin_agent, methods=['POST'])
    # Allow a logged-in Agent to sign-out with Emwebed Server as well.
    app.add_url_rule('/agent/auth/signout', 'ag_signout_handler',
                     signout_agent, methods=['POST'])

    # We've to add this - unless we figure out a Pythonic way of verifying
    # Firebase tokens on Agent side - without using Firebase Admin SDK.
    # Goal is not to use Firebase Admin SDK on Agent.
    # It might be inevitable and will save a trip to Emwebed Server but
    # we don't know what side-effects it will cause and we've setup the
    # rules to stop any possible invasive db queries from Agents.

    # For example - will Agent can change the data related to agents and
    # other users. Ieally - the service-account used to initialize Firebase
    # client should have granular access defined. But need to VERIFY that.

    app.add_url_rule('/agent/verify/token', 'ag_token_verifier',
                     verify_agent_token, methods=['POST'])

    app.add_url_rule('/agent/status/<command_type>', 'ag_status_handler',
                     agent_status_handler, methods=['POST'])


def register_agent_views(app):
    agent_views(app)
    # this is home page - render a nice welcome page here
    app.add_url_rule('/', 'index', index, methods=['GET'])

    app.add_url_rule('/submit/login', 'submit_login',
                     submit_login, methods=['GET', 'POST'])

    app.add_url_rule('/userlogin', 'user_login',
                     do_user_login, methods=['GET', 'POST'])

    app.add_url_rule('/verifyAgent', 'do_agent_verification',
                     do_agent_verification, methods=['GET'])


# All Agent endpoints must go-through a stringent User-id/Agent-id/
# Access rules.
def auth_verify_access(agent_id, current_user_id):
    pass


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000, Debug=True)
