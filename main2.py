#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import requests
import hmac
import hashlib
from urllib import parse
import json
import datetime


ROOT_URL = 'https://www.mxc.ceo'


def _get_server_time():
    return int(time.time())


def _sign(method, path, original_params=None):
    params = {
        'api_key': API_KEY,
        'req_time': _get_server_time(),
    }
    if original_params is not None:
        params.update(original_params)
    params_str = '&'.join('{}={}'.format(k, params[k]) for k in sorted(params))
    to_sign = '\n'.join([method, path, params_str])
    params.update({'sign': hmac.new(SECRET_KEY.encode(), to_sign.encode(), hashlib.sha256).hexdigest()})
    return params


def get_symbols():
    """marget data"""
    method = 'GET'
    path = '/open/api/v2/market/symbols'
    url = '{}{}'.format(ROOT_URL, path)
    params = {'api_key': API_KEY}
    response = requests.request(method, url, params=params)
    print(response.json())
    for i in response.json()['data']:
        if i['symbol'] == "YFX_USDT":
            print(i)

    print(len(response.json()['data']))


def get_rate_limit():
    """rate limit"""
    method = 'GET'
    path = '/open/api/v2/common/rate_limit'
    url = '{}{}'.format(ROOT_URL, path)
    params = {'api_key': API_KEY}
    response = requests.request(method, url, params=params)
    print(response.json())


def get_timestamp():
    """get current time"""
    method = 'GET'
    path = '/open/api/v2/common/timestamp'
    url = '{}{}'.format(ROOT_URL, path)
    params = {'api_key': API_KEY}
    response = requests.request(method, url, params=params)
    print(response.json())


def get_ticker(symbol):
    """get ticker information"""
    method = 'GET'
    path = '/open/api/v2/market/ticker'
    url = '{}{}'.format(ROOT_URL, path)
    params = {
        'api_key': API_KEY,
        'symbol': symbol,
    }
    response = requests.request(method, url, params=params)
    # print(response.json())
    return response.json()


def get_depth(symbol, depth):
    """获market depth"""
    method = 'GET'
    path = '/open/api/v2/market/depth'
    url = '{}{}'.format(ROOT_URL, path)
    params = {
        'api_key': API_KEY,
        'symbol': symbol,
        'depth': depth,
    }
    response = requests.request(method, url, params=params)
    print(response.json())


def get_deals(symbol, limit):
    """get deals records"""
    method = 'GET'
    path = '/open/api/v2/market/deals'
    url = '{}{}'.format(ROOT_URL, path)
    params = {
        'api_key': API_KEY,
        'symbol': symbol,
        'limit': limit,
    }
    response = requests.request(method, url, params=params)
    print(response.json())


def get_kline(symbol, interval):
    """k-line data"""
    method = 'GET'
    path = '/open/api/v2/market/kline'
    url = '{}{}'.format(ROOT_URL, path)
    params = {
        'api_key': API_KEY,
        'symbol': symbol,
        'interval': interval,
    }
    response = requests.request(method, url, params=params)
    print(response.json())


def get_account_info():
    """account information"""
    method = 'GET'
    path = '/open/api/v2/account/info'
    url = '{}{}'.format(ROOT_URL, path)
    params = _sign(method, path)
    response = requests.request(method, url, params=params)
    print(response.json())


def place_order(symbol, price, quantity, trade_type, order_type):
    """place order"""
    method = 'POST'
    path = '/open/api/v2/order/place'
    url = '{}{}'.format(ROOT_URL, path)
    params = _sign(method, path)
    data = {
        'symbol': symbol,
        'price': price,
        'quantity': quantity,
        'trade_type': trade_type,
        'order_type': order_type,
    }
    response = requests.request(method, url, params=params, json=data)
    # print(response.json())
    return response.json()


def batch_orders(orders):
    """batch order"""
    method = 'POST'
    path = '/open/api/v2/order/place_batch'
    url = '{}{}'.format(ROOT_URL, path)
    params = _sign(method, path)
    response = requests.request(method, url, params=params, json=orders)
    print(response.json())


def cancel_order(order_id):
    """cancel in batch"""
    origin_trade_no = order_id
    if isinstance(order_id, list):
        origin_trade_no = parse.quote(','.join(order_id))
    method = 'DELETE'
    path = '/open/api/v2/order/cancel'
    url = '{}{}'.format(ROOT_URL, path)
    params = _sign(method, path, original_params={'order_ids': origin_trade_no})
    if isinstance(order_id, list):
        params['order_ids'] = ','.join(order_id)
    response = requests.request(method, url, params=params)
    print(response.json())


def get_open_orders(symbol):
    """current orders"""
    method = 'GET'
    path = '/open/api/v2/order/open_orders'
    original_params = {
        'symbol': symbol,
    }
    url = '{}{}'.format(ROOT_URL, path)
    params = _sign(method, path, original_params=original_params)
    response = requests.request(method, url, params=params)
    print(response.json())


def get_all_orders(symbol, trade_type):
    """order list"""
    method = 'GET'
    path = '/open/api/v2/order/list'
    original_params = {
        'symbol': symbol,
        'trade_type': trade_type,
    }
    url = '{}{}'.format(ROOT_URL, path)
    params = _sign(method, path, original_params=original_params)
    response = requests.request(method, url, params=params)
    print(response.json())


def query_order(order_id):
    """query order"""
    origin_trade_no = order_id
    if isinstance(order_id, list):
        origin_trade_no = parse.quote(','.join(order_id))
    method = 'GET'
    path = '/open/api/v2/order/query'
    url = '{}{}'.format(ROOT_URL, path)
    original_params = {
        'order_ids': origin_trade_no,
    }
    params = _sign(method, path, original_params=original_params)
    if isinstance(order_id, list):
        params['order_ids'] = ','.join(order_id)
    response = requests.request(method, url, params=params)
    print(response.json())


def get_deal_orders(symbol):
    """account deal records"""
    method = 'GET'
    path = '/open/api/v2/order/deals'
    url = '{}{}'.format(ROOT_URL, path)
    original_params = {
        'symbol': symbol,
    }
    params = _sign(method, path, original_params=original_params)
    response = requests.request(method, url, params=params)
    print(response.json())


def get_deal_detail(order_id):
    """deal detail"""
    method = 'GET'
    path = '/open/api/v2/order/deal_detail'
    url = '{}{}'.format(ROOT_URL, path)
    original_params = {
        'order_id': order_id,
    }
    params = _sign(method, path, original_params=original_params)
    response = requests.request(method, url, params=params)
    print(response.json())




if __name__ == '__main__':
    global API_KEY
    global SECRET_KEY
    # API_KEY = 'mx0NdVdSj4qqJKOQHz'
    # SECRET_KEY = '10cf20ec7bb842bb842151bc63870aa0'

    API_KEY = sys.argv[1]
    SECRET_KEY = sys.argv[2]
    USDT = int(sys.argv[3])
    rate = int(sys.argv[4])
    multipler = float(sys.argv[5])
    sleep = int(sys.argv[6])
    symbol = sys.argv[7]

    pair = symbol + '_USDT'
    # get_symbols()
    # sys.exit(0)
    # get_rate_limit()
    # get_timestamp()

    # get_depth('BTC_USDT', 5)
    # get_deals('BTC_USDT', 5)
    # get_kline('BTC_USDT', '1m')
    # get_account_info()
    i = int(round(time.time() * 1000))
    print("start", int(round(time.time() * 1000)) - i)
    y = get_ticker(pair)
    print("Get ASK price", int(round(time.time() * 1000)) - i)
    order = float(y['data'][0]['ask']) * (rate + 100) * 0.01
    count = int(USDT / order)
    res = place_order(pair, str(order), count, 'BID', 'LIMIT_ORDER')
    print(res)
    if res['code'] == 200:
        print("BID done", int(round(time.time() * 1000)) - i)
        if sleep != 0:
            time.sleep(sleep)
        res = place_order(pair, str(order * multipler), count, 'ASK', 'LIMIT_ORDER')
        print(res)
        if res['code'] == 200:
            print("Placed ASK", int(round(time.time() * 1000)) - i)
    # place_order('BTC_USDT', 7900, 0.1, 'BID', 'LIMIT_ORDER')
    # cancel_order('cfc5a95618f****6d751dd04b2')
    # cancel_order(['cfc5a95618f****d751dd04b2', 'b956dfc923d***31b383c9d'])
    # batch_orders([
    #     {
    #         'symbol': 'BTC_USDT',
    #         'price': '7900',
    #         'quantity': '1',
    #         'trade_type': 'BID',
    #         'order_type': 'LIMIT_ORDER',
    #     },
    #     {
    #         'symbol': 'BTC_USDT',
    #         'price': '7901',
    #         'quantity': '1',
    #         'trade_type': 'ASK',
    #         'order_type': 'LIMIT_ORDER',
    #     },
    # ])
    # get_open_orders('ADA_USDT')
    # get_all_orders('ADA_USDT', 'BID')
    # query_order('ccbd62471d***dd109903e')
    # query_order(['ec72970d2****8264d7e86e', 'fd4d614ee4cf46***c7c82c0'])
    # get_deal_orders('BTC_USDT')
    # get_deal_detail('ccbd62471d*****ddd109903e')


