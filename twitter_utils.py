import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

def get_request_token():
    client = oauth2.Client(consumer)

    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print("An error occuered getting the request token from twitter.")

    # Get the request token and parse the query string
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oauth_verifier(request_token):
    # Ask user to autorize our app and give us pin code
    print("Go to the following site in your browser:")
    print()
    return input("What is your PIN? ")

def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token'])

def get_access_token(request_token, oauth_verifier):
     # Create a Token object which contains the request token and verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # Create a client with our consumer (our app) and the newly created (and verified) token
    client = oauth2.Client(consumer, token)

    # Ask Twitter for an access token, and Twitter knows it should give us since we have verfied request token
    response, content = client.request(constants.ACCESS_TOKEN, "POST")
    return dict(urlparse.parse_qsl(content.decode("utf-8")))
