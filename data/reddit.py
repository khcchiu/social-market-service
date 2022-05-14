import logging
import os

import asyncpraw
import pandas as pd
import requests
import yaml

log = logging.getLogger(__name__)

LIMIT = 100
reddit_config = yaml.load(open(os.getcwd() + '/resources/config.yml'), Loader=yaml.FullLoader)['reddit']
session = requests.Session()
session.verify = False  # Disable SSL
reddit = asyncpraw.Reddit(client_id=reddit_config['client_id'],
                          client_secret=reddit_config['client_secret'],
                          user_agent=reddit_config['user_agent'],
                          username=reddit_config['username'])


async def get_subreddit(subreddits):
    data = []
    ids = []

    log.info('Retrieving subreddits: ' + str(subreddits))
    for subreddit in subreddits:
        hot_posts = await reddit.subreddit(subreddit)
        print(hot_posts.hot())
        async for post in hot_posts.hot(limit=LIMIT):
            if post.id not in ids:
                ids.append(post.id)
                data.append([post.title, post.score, post.id, post.subreddit, post.url, post.selftext, post.created])

    return pd.DataFrame(data, columns=['title', 'score', 'id', 'subreddit', 'url', 'body', 'created'])
