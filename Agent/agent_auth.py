import requests
from agent_settings import *

# Google Identity APIs
_verify_token_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken'
_verify_password_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword'
_password_reset_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/resetPassword'
_verify_email_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo'
_email_sign_in_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/emailLinkSignin'
_get_account_info_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo'


class AgentAuthentication:
    def __init__(self, parent=None):
        self.token_id = None
        self.api_key = None
        self.is_authenticated = False
        self.parent = parent

        self._current_user = None

    def sign_in_email_password(self, userid, passphrase, api_key, agent_settings):
        uri_params = {'key': api_key}
        body = {'email': userid, 'password': passphrase}
        print("Signing in(user: {})".format(userid))

        response = requests.post(_verify_password_url,
                                 params=uri_params, json=body)
        response.raise_for_status()
        if response:
            print("Fetching User-details on Firebase...\n")
            self.api_key = api_key
        else:
            print("Invalid username or password")
        token = response.json().get('idToken')

        self.token_id = token
        body = {
            'idToken': token,
            'agent': agent_settings
        }

        full_uri = EMWEBED_SERVER_URI +  EMWEBED_SERVER_AGENT_ENDPOINTS['login']

        response = requests.post(full_uri, json=body)
        response.raise_for_status()
        if response:
            print("Signed-up Successfully (user: {})".format(userid))
            self.is_authenticated = True
        else:
            self.is_authenticated = False

    def sign_out(self, userid):
        self._current_user = None
        self.is_authenticated = False
        self.token_id = None
        self.api_key = None

        # notify parent object about this signed-out status
        pass

if __name__ == "__main__":
    user = "too@xyz.com"
    password = 'blabla'
    ag = AgentAuthentication()
    ag.sign_in_email_password(
        user, password, "AIzaSyD2REY8_lmDFUZPbmFzi1LsI6C4hWTSkkc")

