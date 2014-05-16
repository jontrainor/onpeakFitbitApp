CONSUMER_KEY = '9a018a262bf848fe8f39687af7da9ae7'
CONSUMER_SECRET = 'd4f554ffc17c4d62b68d4bf24cd81372'

import os
from flask import Flask, url_for, redirect, session, request
from fitbit import Fitbit
from fitbit.api import FitbitOauthClient

app = Flask(__name__)
app.secret_key = os.urandom(24)

oauth_client = FitbitOauthClient(CONSUMER_KEY, CONSUMER_SECRET, callback_uri='http://localhost:5000/oauth_authorized')

@app.route('/')
def index():
	if 'fitbit_access_token' not in session:
		return redirect(url_for('login'))
	client = Fitbit(CONSUMER_KEY, CONSUMER_SECRET, resource_owner_key=session['fitbit_access_token']['oauth_token'], resource_owner_secret=session['fitbit_access_token']['oauth_token_secret'])
	return str(client.user_profile_get())

@app.route('/login')
def login():
	oauth_client.fetch_request_token()
	return redirect(oauth_client.authorize_token_url())

@app.route('/oauth_authorized')
def oauth_authorized():
	oauth_token = request.args.get('oauth_token')
	oauth_verifier = request.args.get('oauth_verifier')
	access_token = oauth_client.fetch_access_token(oauth_verifier)
	session['fitbit_access_token'] = access_token
	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	if 'fitbit_access_token' in session:
		del session['fitbit_access_token']
	return redirect(url_for('index'))



if __name__ == "__main__":
	app.run(debug=True)