import json
import os
import praw

def set_credentials_env_var(path_json_creds):
    with open(path_json_creds) as f:
        creds = json.load(f)
    os.environ["CLIENT_ID"] = creds["CLIENT_ID"]
    os.environ["CLIENT_SECRET"] = creds["CLIENT_SECRET"]
    os.environ["CLIENT_AGENT"] = creds["CLIENT_AGENT"]


def get_reddit_client():
    reddit_client = praw.Reddit(client_id = os.environ["CLIENT_ID"],
                         client_secret = os.environ["CLIENT_SECRET"],
                         user_agent = os.environ["CLIENT_AGENT"])
    return reddit_client

