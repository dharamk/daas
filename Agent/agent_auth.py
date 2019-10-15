import requests
from agent_settings import *
from datetime import datetime


# Google Identity APIs
_verify_token_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken'
_verify_password_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword'
_password_reset_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/resetPassword'
_verify_email_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo'
_email_sign_in_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/emailLinkSignin'
_get_account_info_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo'

_refresh_token_url = 'https://securetoken.googleapis.com/v1/token'


def get_timestamp():
    """
    Returns current timestamp value in integer.
    """
    return int(datetime.timestamp(datetime.now().replace(microsecond=0)))


class AgentAuthentication:
    def __init__(self, parent=None):
        self.id_token = None
        self.token_expiry_duration = 0
        self.token_created_timestamp = None

        self.api_key = None
        self.is_authenticated = False
        self.parent = parent

        self._current_user = None
        self._user_login_info = None

    def _is_token_expired(self, id_token=None):
        if self.id_token:
            raise ValueError
        pass

    def refresh_token(self):
        uri_params = {
            'key': self.api_key
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = 'grant_type=refresh_token&refresh_token=' + self.refresh_token
        response = requests.post(_refresh_token_url,
                                 params=uri_params, data=data, headers=headers)

        response.raise_for_status()
        json_response = response.json()
        self.id_token = json_response.get('id_token')
        uid = json_response.get('user_id')
        self.token_expires_at = get_timestamp() + int(json_response['expires_in'])

        pass

    def get_id_token(self):
        """
        Other classes and functions will call this function
        to get a valid id-token. This is not replacement for
        sign-in function.

        raise ValueError if the user has not signed-in using sign-in
        function earlier.
        """
        if self._current_user:
            raise ValueError("User not logged-in")

        if self.token_expires_at <= get_timestamp():
            self.refresh_token()

        return self.id_token

    def sign_in_email_password(self, userid, passphrase, api_key, agent_settings):
        uri_params = {'key': api_key}
        body = {
            'email': userid,
            'password': passphrase,
            'returnSecureToken': True
        }

        print("Signing in(user: {})".format(userid))

        # Verify Password and email from Firebase Auth Service
        response = requests.post(_verify_password_url,
                                 params=uri_params, json=body)
        response.raise_for_status()
        if not response:
            raise ValueError("Invalid Username or Password")

        print("Fetching User-details on Firebase...\n")
        self.api_key = api_key

        json_response = response.json()

        token = json_response.get('idToken')
        uid = json_response.get('localId')

        self.refresh_token = json_response.get('refreshToken')
        # self.token_expiry_duration = json_response.get('expiresIn')
        self.token_expires_at = get_timestamp() + int(json_response.get('expiresIn'))
        self._current_user = uid

        # getUserInfo request from Firebase Auth Service
        body = {'idToken': token}
        response = requests.post(_get_account_info_url,
                                 params=uri_params, json=body)

        response.raise_for_status()
        if not response:
            raise ValueError("Invalid Response while fetching UserInfo")

        self._user_login_info = response.json()

        # print(response.json())
        # print(token)

        self.id_token = token
        body = {
            'idToken': token,
            'uid': uid,
            'agent': agent_settings
        }

        full_uri = EMWEBED_SERVER_URI + EMWEBED_SERVER_AGENT_ENDPOINTS['login']

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
        self.id_token = None
        self.api_key = None
        self._user_login_info = None

        # notify parent object about this signed-out status
        pass


if __name__ == "__main__":
    user = "too@xyz.com"
    password = 'blabla'
    ag = AgentAuthentication()
    ag.sign_in_email_password(
        user, password, "AIzaSyD2REY8_lmDFUZPbmFzi1LsI6C4hWTSkkc")
