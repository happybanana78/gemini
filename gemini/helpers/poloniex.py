import logging
import time

import pandas as pd
import requests

logger = logging.getLogger(__name__)


def get_now(pair):
    """
    Return last info for crypto currency pair
    :param pair:
    :return:
    """
    return requests.get(
        'https://poloniex.com/public?command=returnTicker').json()[pair]


def get_past(pair, period, days_history=30):
    """
    Return historical charts data from poloniex.com
    """
    end = int(time.time())
    start = end - (24 * 60 * 60 * days_history)

    url = 'https://api.poloniex.com/markets/{0}/candles?startTime={1}&interval={2}'
    url = url.format(pair, start, period)
    response = requests.get(url)
    return response.json()


def load_dataframe(pair, period, days_history=30):
    """
    Return historical charts data from poloniex.com
    :param pair:
    :param period:
    :param days_history:
    :param timeframe: H - hour, D - day, W - week, M - month
    :return:
    """
    data = get_past(pair, period, days_history)
    if 'error' in data:
        raise Exception("Bad response: {}".format(data['error']))

    df = pd.DataFrame(data)
    df[9] = pd.to_datetime(df[9], unit='ms')
    df = df.set_index([9])

    return df
