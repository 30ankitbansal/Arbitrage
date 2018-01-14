# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import datetime
import logging
from urllib.parse import urlencode
import requests
import sys
import time
import pickle
import os.path
from collections import OrderedDict
import uuid

dir = os.path.dirname(os.path.abspath(__file__)) + "/"


class Bitcoin_co_id(object):
    ETH_ADDRESS = ""
    BTC_ADDRESS = ""
    BTC_BALANCE = 0
    ETH_BALANCE = 0

    def __init__(self, key=None, secret=None):
        self.logger = logging.getLogger("Bitcoin_co_id")
        self.BASE_URL = "https://vip.bitcoin.co.id/tapi"
        self.handler = logging.FileHandler(dir + 'logs/bitcoin_co_id.log')
        self.is_continuous = False
        self.key = key
        self.secret = secret
        self._init_logger()
        self.current_pair = 'eth_btc'
        self.summary = None
        self.bet_started = False

    def _init_logger(self):
        self.logger.setLevel(logging.INFO)
        self.handler.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def _format_log(self, string, level):
        return "{} {}: {}".format(level, datetime.datetime.now(), string)

    def _parse_summary(self, summary):
        s = {}
        try:
            s['Bid'] = summary['ticker']['buy']
            s['Ask'] = summary['ticker']['sell']
            return s
        except Exception as e:
            self.logger.info(self._format_log(e, "ERROR"))
            return s

    def send_bets(self, **params):  # place order
        """
                :param params:
                 contains four parameters
                 1 type : buy or sell
                 2 price : price of currency
                 3 btc: amount of btc sell
                 4 eth: amount of eth sell
        """
        if self.key and self.secret:
            data = OrderedDict({'method': 'trade', 'nonce': str(int(time.time()) + 86400), 'pair': self.current_pair,
                                'type': params['type'], 'price': params['price'], 'btc': params['btc'], 'eth': params['eth']})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                data = data['return']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_balance(self):
        if self.key and self.secret:
            data = OrderedDict({'method': 'getInfo', 'nonce': str(int(time.time()) + 86400)})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                self.BTC_BALANCE = data['return']['balance']['btc']
                self.ETH_BALANCE = data['return']['balance']['eth']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_transactions(self):
        if self.key and self.secret:
            data = OrderedDict({'method': 'transHistory', 'nonce': str(int(time.time()) + 86400)})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                data = data['return']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_order(self, orderId):
        if self.key and self.secret:
            data = OrderedDict(
                {'method': 'getOrder', 'pair': self.current_pair, 'order_id': orderId,
                 'nonce': str(int(time.time()) + 86400)})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                data = data['return']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_orders(self):
        if self.key and self.secret:
            data = OrderedDict({'method': 'orderHistory', 'pair': self.current_pair,
                                'nonce': str(int(time.time()) + 86400)})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                data = data['return']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def open_orders(self):
        if self.key and self.secret:
            data = OrderedDict({'method': 'openOrders', 'pair': self.current_pair,
                                'nonce': str(int(time.time()) + 86400)})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                data = data['return']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_trades(self):
        if self.key and self.secret:
            data = OrderedDict({'method': 'tradeHistory', 'nonce': str(int(time.time()) + 86400), 'pair': self.current_pair})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                data = data['return']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def cancel_limit(self, **params):
        if self.key and self.secret:
            data = OrderedDict(
                {'method': 'cancelOrder', 'pair': self.current_pair, 'order_id': params['order_id'],
                 'type': params['type'], 'nonce': str(int(time.time()) + 86400)})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                data = data['return']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_wallet_address(self):
        if self.key and self.secret:
            data = OrderedDict({'method': 'getInfo', 'nonce': str(int(time.time()) + 86400)})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                self.BTC_BALANCE = data['return']['address']['btc']
                self.ETH_BALANCE = data['return']['address']['eth']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def send_coin(self, **params):  # Withdraw coin
        """
        :param params:
         contains four parameters
         1 currency ex ETH
         2 withdraw_amount
         3 withdraw_address
        """
        if self.key and self.secret:
            data = OrderedDict(
                {'method': 'withdrawCoin', 'nonce': str(int(time.time()) + 86400), 'currency': params['currency'],
                 'withdraw_amount': params['withdraw_amount'], 'withdraw_address': params['withdraw_address'],
                 'request_id': uuid.uuid4().hex})
            encoded_data = bytearray(urlencode(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {"Key": self.key, "Sign": sign}
            data = json.loads(requests.post(self.BASE_URL, data=data, headers=headers).text)
            if isinstance(data, dict) and data['success'] == 1:
                data = data['return']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_order_book(self):
        ret = requests.get('https://vip.bitcoin.co.id/api/' + str(self.current_pair) + '/depth',
                           headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return json.loads(data)

    def last_trade(self):
        ret = requests.get('https://vip.bitcoin.co.id/api/' + str(self.current_pair) + '/trades',
                           headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return json.loads(data)

    def get_summary(self):  # ticker data
        ret = requests.get('https://vip.bitcoin.co.id/api/' + str(self.current_pair) + '/ticker',
                           headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        print(data)
        self.logger.info(self._format_log(data, "INFO"))
        return self._parse_summary(json.loads(data))


if __name__ == "__main__":
    bcd = Bitcoin_co_id()
    print(bcd.get_summary())
    