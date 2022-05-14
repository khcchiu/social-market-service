import logging
import os

import pandas as pd
import requests
from searchtweets import load_credentials, collect_results
from searchtweets.api_utils import gen_request_parameters

log = logging.getLogger(__name__)

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

search_args = load_credentials(os.getcwd() + '/resources/config.yml',
                               yaml_key='search_tweets_v2',
                               env_overwrite=False)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_tweets(keyword):
    print('Retrieving tweet for keyword: ' + keyword)
    rule = gen_request_parameters(keyword, results_per_call=100)  # testing with a sandbox account
    tweets = collect_results(rule, result_stream_args=search_args)

    df = pd.DataFrame(tweets)
    return df


def get_count(keyword):
    json_response = connect_to_endpoint("https://api.twitter.com/2/tweets/counts/recent",
                                        {'query': keyword, 'granularity': 'hour'})
    df = pd.DataFrame(json_response['data'])
    return df
