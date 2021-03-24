from database import Database
from user import User
from twitter_utils import consumer, get_request_token, get_oauth_verifier, get_access_token


try:
    Database.initialize(user="postgres", password="postgres",
                        database="learning", host="localhost")
except Exception as e:
    print("Database Initialized failed")
    print(e)

# Search if enterd email has been registerd
email = input("Enter your email: ")
user = User.load_from_db_by_email(email)

# When user is not registerdampeid
if not user:
    
    # Use the client to perform a request for the request token
    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)
    
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    user = User(email, first_name, last_name,
            access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

tweets = user.twitter_request("https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images")

for tweet in tweets["statuses"]:
    print(tweet["text"])

