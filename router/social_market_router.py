from fastapi import APIRouter
from starlette.responses import Response

from data.reddit import get_subreddit
from data.trends import get_interest_over_time, get_related_queries
from data.twitter import get_tweets, get_count

router = APIRouter()


@router.get('/reddit/{subreddit}')
async def get_reddit(subreddit: str):
    df_subreddits = await get_subreddit([subreddit])
    return Response(content=df_subreddits.to_json(orient='records', default_handler=str), media_type='application/json')


@router.get('/trends/interest-over-time/{keyword}')
async def get_trends_interest_over_time(keyword: str):
    df_interest_over_time = get_interest_over_time([keyword])
    return Response(content=df_interest_over_time.to_json(date_format='iso'), media_type='application/json')


@router.get('/trends/related-queries/{keyword}')
async def get_trends_related_queries(keyword: str):
    df_related_queries = get_related_queries([keyword])
    return Response(content=df_related_queries.to_json(), media_type='application/json')


@router.get('/twitter/tweets/{keyword}')
async def get_twitter_tweets(keyword: str):
    df_tweets = get_tweets(keyword)
    return Response(content=df_tweets.to_json(orient='records'), media_type='application/json')


@router.get('/twitter/tweet-count/{keyword}')
async def get_twitter_tweet_count(keyword: str):
    return Response(content=get_count(keyword).to_json(orient='records'), media_type='application/json')
