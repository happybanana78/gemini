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
    :param timeframe: MINUTE_1, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR_1, HOUR_2, HOUR_4, HOUR_6, HOUR_12, DAY_1, DAY_3, WEEK_1, MONTH_1
    :return:
    """
    data = get_past(pair, period, days_history)
    if 'error' in data:
        raise Exception("Bad response: {}".format(data['error']))
    
    """
    Assign column names
    """
    column_names = ['low', 'high', 'open', 'close', 'amount', 'volume', 'buyTakerAmount', 'buyTakerVolume', 'tradeCount', 'date', 'weightedAverage', 'interval', 'startTime', 'closeTime']

    df = pd.DataFrame(data, columns=column_names)
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df = df.set_index(['date'])

    return df

load_dataframe('BTC_USDT', 'DAY_1', 100)