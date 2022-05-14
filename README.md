# social-market-service

start cmd: uvicorn main:app --port 8081

create resources/config.yml with below details

reddit:
client_id: ***
client_secret: ***
user_agent: 'testscript by u/fakebot3'
username: fakebot3

search_tweets_v2:
endpoint: https://api.twitter.com/2/tweets/search/recent
consumer_key: ***
consumer_secret: ***
bearer_token: ***
