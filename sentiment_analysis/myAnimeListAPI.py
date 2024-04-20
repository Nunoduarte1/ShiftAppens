import json
import requests
import secrets
import os



CLIENT_ID = '908f4a0405400da4cc61762f001a19a1'
CLIENT_SECRET = "400013c275d44c98f7387dbbca0c952f117159ab91008ec2b3ab697490bec398"
ACCESS_TOKEN_URL = "https://myanimelist.net/v1/oauth2/token"
ACCESS_AUTH_URL = "https://myanimelist.net/v1/oauth2/authorize"

TOKEN = ''
anime_id = "21" # One Piece

# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str):
    global CLIENT_ID

    url = f'{ACCESS_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
    print(f'Authorise your application by clicking here: {url}\n')


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = ACCESS_TOKEN_URL
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': authorisation_code,
        'code_verifier': code_verifier
        
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    with open('token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token saved in "token.json"')

    return token


def setup_token():
    code_verifier = code_challenge = get_new_code_verifier()
    print_new_authorisation_url(code_challenge)

    authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    token = generate_new_token(authorisation_code, code_verifier)
    return token




#######################################################################



# Send request to the API
def send_get_request(url: str, access_token: str, params = {}):
    #url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
        }, params = params)
    
    response.raise_for_status()
    data = response.json()
    response.close()

    return data


def initConnection():
    global TOKEN

    # creat new token
    if not os.path.exists('token.json'):
        TOKEN = setup_token()
    else:
        # load token
        with open('token.json', 'r') as file:
            TOKEN = json.load(file)


def makeRequest(url):
    initConnection()

    return send_get_request(url, TOKEN['access_token'])

