import requests
from flask import Flask, render_template, session, redirect, request, url_for, g, jsonify
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User
from database import Database


app = Flask(__name__)
app.secret_key = '1234'

@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screen_name(session['screen_name'])


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/login/twitter')
def twitter_login():
    if "screen_name" in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    session['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')
def twitter_auth():
    oauth_verfier = request.args.get("oauth_verifier")
    access_token = get_access_token(session['request_token'], oauth_verfier)
    
    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'], None)
        user.save_to_db()
    session['screen_name'] = user.screen_name
    
    return redirect(url_for('profile')) # [NOTE] url_for('method name')! NOT an endpoint name as an arg. 


@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)


@app.route('/search')
def search():
    query = request.args.get('q')
    uri = "https://api.twitter.com/1.1/search/tweets.json?q={}".format(query)
    tweets = g.user.twitter_request(uri)
    tweet_texts = [{'tweet': tweet["text"], 'label': 'neutral'} for tweet in tweets["statuses"]]
    
    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = r.json()
        tweet['label'] = json_response["label"]
pwd
    return render_template('search.html', content=tweet_texts)


if __name__ == '__main__':
    Database.initialize(user="postgres", password="postgres", host="localhost", database="learning")
    app.run(port=4995, host="0.0.0.0", debug=True)