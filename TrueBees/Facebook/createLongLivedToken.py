import requests
import json

"""
Script to create a long-lived token that avoid frequent access requests.
Execute with the credentials.json in the directory.
"""
with open('credentials.json') as f:
    credentials = json.load(f)
access_token = credentials['access_token']
page_id = credentials['page_id']
app_id = credentials['app_id']
app_secret = credentials["app_secret"]

params = {
    ('grant_type', 'fb_exchange_token'),
    ('client_id', app_id),
    ('client_secret', app_secret),
    ('fb_exchange_token', access_token),
    ('access_token', access_token),
}

response = requests.get('https://graph.facebook.com/oauth/access_token', params=params)
j_res = response.json()
print(j_res.get("access_token"))
