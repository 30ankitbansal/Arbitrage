# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import datetime
import logging
import requests
import sys
import time
import os.path
from bs4 import BeautifulSoup

dir = os.path.dirname(os.path.abspath(__file__)) + "/"


class Southxchange(object):
    ETH_ADDRESS = ""
    BTC_ADDRESS = ""
    BTC_BALANCE = 0
    ETH_BALANCE = 0

    def __init__(self, key=None, secret=None):
        self.logger = logging.getLogger("Southxchange")
        self.BASE_URL = "https://www.southxchange.com/api/"
        self.handler = logging.FileHandler(dir + 'logs/southxchange.log')
        self.is_continuous = False
        self.key = key
        self.secret = secret
        self._init_logger()
        self.current_pair = 'ETH/BTC'
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
            s['Bid'] = summary['Bid']
            s['Ask'] = summary['Ask']
            return s
        except Exception as e:
            self.logger.info(self._format_log(e, "ERROR"))
            return s

    def send_bets(self, **params):  # place order
        """
                :param params:
                 contains four parameters
                 1 type : buy or sell
                 2 price : Optional price in reference currency. If null then order is executed at market price
                 3 amount: Order amount in listing currency
        """
        if self.key and self.secret:
            url = self.BASE_URL + 'placeOrder'
            data = {'nonce': str(int(time.time())),
                    'key': self.key,
                    'listingCurrency': self.current_pair.split('/')[0],
                    'referenceCurrency': self.current_pair.split('/')[1],
                    'type': params['type'],
                    'amount': params['amount'],
                    'limitPrice': params['price']}
            encoded_data = bytearray(json.dumps(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {'Hash': sign, 'Content-Type': 'application/json'}
            content = requests.post(url=url, data=json.dumps(data), headers=headers)
            try:
                soup = BeautifulSoup(content.text, "html.parser")
                title = soup.find('title').text
                return title
            except:
                pass
            self.logger.info(self._format_log(content.text, "INFO"))
            return json.loads(content.text)
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_balance(self):
        if self.key and self.secret:
            url = self.BASE_URL + 'listBalances'
            data = {'nonce': str(int(time.time())), 'key': self.key}
            encoded_data = bytearray(json.dumps(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {'Hash': sign, 'Content-Type': 'application/json'}
            content = requests.post(url=url, data=json.dumps(data), headers=headers)
            try:
                soup = BeautifulSoup(content.text, "html.parser")
                title = soup.find('title').text
                return title
            except:
                pass
            content = json.loads(content.text)
            for data in content:
                if str(data['Currency']).upper() == 'BTC':
                    self.BTC_BALANCE = data['Available']
                elif str(data['Currency']).upper() == 'ETH':
                    self.ETH_BALANCE = data['Available']
            self.logger.info(self._format_log(content, "INFO"))
            return content
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_orders(self):
        if self.key and self.secret:
            url = self.BASE_URL + 'listOrders'
            data = {'nonce': str(int(time.time())),
                    'key': self.key
                    }
            encoded_data = bytearray(json.dumps(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {'Hash': sign, 'Content-Type': 'application/json'}
            content = requests.post(url=url, data=json.dumps(data), headers=headers)
            try:
                soup = BeautifulSoup(content.text, "html.parser")
                title = soup.find('title').text
                return title
            except:
                pass
            self.logger.info(self._format_log(content.text, "INFO"))
            return json.loads(content.text)
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def open_orders(self):
        if self.key and self.secret:
            url = self.BASE_URL + 'listOrders'
            data = {'nonce': str(int(time.time())),
                    'key': self.key
                    }
            encoded_data = bytearray(json.dumps(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {'Hash': sign, 'Content-Type': 'application/json'}
            content = requests.post(url=url, data=json.dumps(data), headers=headers)
            try:
                soup = BeautifulSoup(content.text, "html.parser")
                title = soup.find('title').text
                return title
            except:
                pass
            self.logger.info(self._format_log(content.text, "INFO"))
            return json.loads(content.text)
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def cancel_limit(self, **params):
        if self.key and self.secret:
            url = self.BASE_URL + 'cancelOrder'
            data = {'nonce': str(int(time.time())),
                    'key': self.key,
                    'orderCode': params['orderCode']
                    }
            encoded_data = bytearray(json.dumps(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {'Hash': sign, 'Content-Type': 'application/json'}
            content = requests.post(url=url, data=json.dumps(data), headers=headers)
            try:
                soup = BeautifulSoup(content.text, "html.parser")
                title = soup.find('title').text
                return title
            except:
                pass
            self.logger.info(self._format_log(content.text, "INFO"))
            return json.loads(content.text)
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def cancel_market(self):
        if self.key and self.secret:
            url = self.BASE_URL + 'cancelMarketOrders'
            data = {'nonce': str(int(time.time())),
                    'key': self.key,
                    'listingCurrency': self.current_pair.split('/')[0],
                    'referenceCurrency': self.current_pair.split('/')[1]
                    }
            encoded_data = bytearray(json.dumps(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {'Hash': sign, 'Content-Type': 'application/json'}
            content = requests.post(url=url, data=json.dumps(data), headers=headers)
            try:
                soup = BeautifulSoup(content.text, "html.parser")
                title = soup.find('title').text
                return title
            except:
                pass
            self.logger.info(self._format_log(content.text, "INFO"))
            return json.loads(content.text)
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_wallet_address(self,currency='BTC'):
        if self.key and self.secret:
            url = self.BASE_URL + 'generatenewaddress'
            data = {'nonce': str(int(time.time())), 'currency': currency, 'key': self.key}
            encoded_data = bytearray(json.dumps(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {'Hash': sign, 'Content-Type': 'application/json'}
            content = requests.post(url=url, data=json.dumps(data), headers=headers)
            if currency == 'BTC':
                self.BTC_ADDRESS = content
            elif currency == 'ETH':
                self.ETH_ADDRESS = content
            return content.text
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def send_coin(self, **params):  # Withdraw coin
        """
        :param params:
         contains four parameters
         1 currency ex ETH
         2 address
         3 amount
        """
        if self.key and self.secret:
            url = self.BASE_URL + 'withdraw'
            data = {'nonce': str(int(time.time())),
                    'key': self.key,
                    'currency': params['currency'],
                    'address': params['address'],
                    'amount': params['amount']
                    }
            encoded_data = bytearray(json.dumps(data), 'utf-8')
            sign = hmac.new(bytearray(self.secret, 'utf-8'), msg=encoded_data, digestmod=hashlib.sha512).hexdigest()
            headers = {'Hash': sign, 'Content-Type': 'application/json'}
            content = requests.post(url=url, data=json.dumps(data), headers=headers)
            try:
                soup = BeautifulSoup(content.text, "html.parser")
                title = soup.find('title').text
                return title
            except:
                pass
            self.logger.info(self._format_log(content.text, "INFO"))
            return content.text
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_order_book(self):
        content = requests.get(self.BASE_URL + 'book/' + str(self.current_pair), headers={'User-Agent': 'Mozilla/5.0'})
        try:
            soup = BeautifulSoup(content.text, "html.parser")
            title = soup.find('title').text

            return title
        except:
            pass
        self.logger.info(self._format_log(content.text, "INFO"))
        return json.loads(content.text)

    def last_trade(self):
        content = requests.get(self.BASE_URL + 'trades/' + str(self.current_pair), headers={'User-Agent': 'Mozilla/5.0'})
        try:
            soup = BeautifulSoup(content.text, "html.parser")
            title = soup.find('title').text
            return title
        except:
            pass
        self.logger.info(self._format_log(content.text, "INFO"))
        return json.loads(content.text)

    def get_summary(self):  # ticker data
        content = requests.get(self.BASE_URL + 'price/' + str(self.current_pair), headers={'User-Agent': 'Mozilla/5.0'})
        try:
            soup = BeautifulSoup(content.text, "html.parser")
            title = soup.find('title').text
            return title
        except:
            pass
        self.logger.info(self._format_log(content.text, "INFO"))
        return self._parse_summary(json.loads(content.text))

    def get_all_pair(self):
        content = requests.get(self.BASE_URL + 'markets', headers={'User-Agent': 'Mozilla/5.0'})
        try:
            soup = BeautifulSoup(content.text, "html.parser")
            title = soup.find('title').text
            return title
        except:
            pass
        self.logger.info(self._format_log(content.text, "INFO"))
        return json.loads(content.text)

if __name__ == "__main__":
    sxchange = Southxchange()
    # print(sxchange.send_coin(currency='BTC', amount='1', address=''))
    # print(sxchange.send_bets(type='buy', amount='0', price='0'))
    # print(sxchange.get_balance())
    # print(sxchange.get_wallet_address())
    # print(sxchange.cancel_market())
    # print(sxchange.cancel_limit(orderCode='123423'))
    # print(sxchange.open_orders())
    # print(sxchange.get_orders())
    # print(sxchange.get_order_book())
    # print(sxchange.last_trade())
    # print(sxchange.get_summary())
    # print(sxchange.get_all_pair())
