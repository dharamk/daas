EMWEBED_AGENT_APP_SETTINGS = {
    "aid": "85d988b9c6125716b38002ba076ce041",
    "name": "my-ubuntu-agent_154049",
    "owner": "default",
    "is_shared": True,
    "created_at": "timestamp",
}

EMWEBED_AGENT_APP_USERID = "too@xyz.com"

# agent should store the password on-disk using some bcrypt hashed format
EMWEBED_AGENT_APP_PASSPHRASE = "blabla"

EMWEBED_AGENT_FIREBASE_API_KEY = ""

EMWEBED_SERVER_URL = ""
EMWEBED_SERVER_ONBOARDING_URL = ""

EMWEBED_AGENT_PORT_MIN = 12321
EMWEBED_AGENT_PORT_MAX = 12421

EMWEBED_AGENT_FIREBASE_APP_SETTINGS = {
    "apiKey": "AIzaSyD2REY8_lmDFUZPbmFzi1LsI6C4hWTSkkc",
    "authDomain": "fir-example-252109.firebaseapp.com",
    "databaseURL": "https://fir-example-252109.firebaseio.com",
    "projectId": "firebase-example-252109",
    "storageBucket": "firebase-example-252109.appspot.com",
    "messagingSenderId": "591717006674",
    "appId": "1:591717006674:web:a3c9a1ca10e9d20b928e8b"
}

EMWEBED_SERVER_URI = 'http://127.0.0.1:5000/'

EMWEBED_SERVER_AGENT_ENDPOINTS = {
    "login": 'agent/user/login',
    "logout": 'agent/user/logout',
    "connection_status": 'agent/status/connection',
    "service_status": 'agent/status/service',
    "device_list": 'agent/status/devicelist',
    "device_info": 'agent/status/deviceinfo'
}
