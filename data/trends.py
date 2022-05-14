import logging

import pandas as pd
from pytrends.exceptions import ResponseError
from pytrends.request import TrendReq

log = logging.getLogger(__name__)

pytrends = TrendReq()


def get_interest_over_time(keywords):
    res = pd.DataFrame()

    log.info('Retrieving interest over time for keywords: ' + str(keywords))
    for keyword in keywords:
        if keyword.isupper():
            keyword = keyword + ' stock'
        try:
            pytrends.build_payload(kw_list=[keyword], timeframe='now 7-d')
        except ResponseError as e:
            log.error(e.response)
            continue
        interest_over_time = pytrends.interest_over_time()
        if res.empty:
            res = interest_over_time
        elif keyword in interest_over_time.columns:
            res[keyword] = interest_over_time[keyword]

    return res


def get_related_queries(keywords):
    pytrends.build_payload(kw_list=keywords)
    log.info('Retrieving related queries for keywords: ' + str(keywords))
    return pd.DataFrame(pytrends.related_queries())
