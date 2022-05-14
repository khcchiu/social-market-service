import os

import matplotlib.pyplot as plt
import pandas as pd
import requests

bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/counts/recent"

# Optional params: start_time,end_time,since_id,until_id,next_token,granularity
query_params = {'query': 'Russia Sanctions', 'granularity': 'hour'}


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    df = pd.DataFrame(json_response['data'])
    df.start = pd.to_datetime(df.start).dt.strftime('%Y-%m-%d')
    df.set_index('start').plot()
    plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    main()
