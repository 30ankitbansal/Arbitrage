# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import datetime
import logging
import threading
import time
import urllib
from urllib.parse import urlencode
import requests
import sys
import time
import pickle
import os.path

dir = os.path.dirname(os.path.abspath(__file__)) + "/"


class Livecoin(object):
    ETH_ADDRESS = ""
    BTC_ADDRESS = ""
    LTC_ADDRESS = ""
    DASH_ADDRESS = ""
    BTC_BALANCE = 0
    ETH_BALANCE = 0
    LTC_BALANCE = 0
    DASH_BALANCE = 0

    def __init__(self, key=None, secret=None):
        self.logger = logging.getLogger("Bittrex")
        self.BASE_URL = "https://livecoin.com/api/"
        self.handler = logging.FileHandler(dir + 'logs/livecoin.log')
        self.is_continuous = False
        self.key = key
        self.secret = secret
        self._init_logger()
        self.current_pair = 'ETH/BTC'
        self.summary = None
        self.currency_list = []
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
            items = [
                "Ask",
                "Bid",
            ]
            for item in items:
                s[item.lower()] = summary['result'][0][item]
            return s
        except Exception as e:
            self.logger.info(self._format_log(e, "ERROR"))
            return s

    def send_bets(self, **params):  # place order
        a = {'sell': 'selllimit', 'buy': 'buylimit'}
        params['market'] = self.current_pair
        if self.key and self.secret:
            url = 'https://bittrex.com/api/v1.1/market/'
            url += a[params['side']] + '?' + urlencode(params)
            url += '&apikey=' + self.key
            url += '&nonce=' + str(int(time.time()))
            # print(url)
            signature = hmac.new(self.secret.encode('utf-8'), url.encode('utf-8'), hashlib.sha512).hexdigest()
            headers = {'apisign': signature}
            # print(headers)
            content = requests.post(url, headers=headers).text
            self.logger.info(self._format_log(content, "INFO"))
            return content
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_balance(self):
        if self.key and self.secret:
            data = OrderedDict({'currency': 'BTC,ETH'})
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "payment/balances?currency=" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign}
            data = json.loads(requests.get(url, headers=headers).text)
            for content in data:
                if content['currency'] == 'BTC' and content['type'] == 'available':
                    self.BTC_BALANCE = content['value']
                elif content['currency'] == 'ETH' and content['type'] == 'available':
                    self.ETH_BALANCE = content['value']
            self.logger.info(self._format_log(content, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_transactions(self, start, end):
        if self.key and self.secret:
            data = OrderedDict({'start': start, 'end': end})
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "/payment/history/transactions?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign}
            data = json.loads(requests.get(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_order(self, orderId):
        if self.key and self.secret:
            data = OrderedDict({'orderId': orderId})
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "exchange/order?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign}
            data = json.loads(requests.get(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_orders(self, orderId):
        if self.key and self.secret:
            data = OrderedDict({})
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "exchange/client_orders?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign}
            data = json.loads(requests.get(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_trades(self, orderId):
        if self.key and self.secret:
            data = OrderedDict({})
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "exchange/trades?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign}
            data = json.loads(requests.get(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def buy_market(self, currencyPair, quantity):
        if self.key and self.secret:
            data = OrderedDict(sorted([('currencyPair', currencyPair), ('quantity', quantity)]))
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "/exchange/buymarket?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}
            data = json.loads(requests.post(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def sell_market(self, currencyPair, quantity):
        if self.key and self.secret:
            data = OrderedDict(sorted([('currencyPair', currencyPair), ('quantity', quantity)]))
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "/exchange/sellmarket?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}
            data = json.loads(requests.post(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def sell_limit(self, currencyPair, quantity, price):
        if self.key and self.secret:
            data = OrderedDict(sorted([('currencyPair', currencyPair), ('quantity', quantity), ('price', price)]))
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "/exchange/selllimit?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}
            data = json.loads(requests.post(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def buy_limit(self, currencyPair, quantity, price):
        if self.key and self.secret:
            data = OrderedDict(sorted([('currencyPair', currencyPair), ('quantity', quantity), ('price', price)]))
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "/exchange/buylimit?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}
            data = json.loads(requests.post(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def cancel_limit(self, currencyPair, orderId):
        if self.key and self.secret:
            data = OrderedDict(sorted([('currencyPair', currencyPair), ('orderId', orderId)]))
            encoded_data = urllib.urlencode(data)
            url = self.BASE_URL + "/exchange/cancellimit?" + encoded_data + '&nonce=' + str(int(time.time()))
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}
            data = json.loads(requests.post(url, headers=headers).text)
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_wallet_address(self, currency="BTC"):
        if self.key and self.secret:
            url = self.BASE_URL + "/payment/get/address" + currency + '?' + self.key + '&nonce=' + str(int(time.time()))
            data = OrderedDict({})
            encoded_data = urllib.urlencode({'currencyPair': currency})
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign}
            data = json.loads(requests.get(url, headers=headers).text)
            if currency == 'BTC':
                self.BTC_ADDRESS = data
            elif currency == 'ETH':
                self.ETH_ADDRESS = data
            self.logger.info(self._format_log(content, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def send_coin(self, **params):  # Withdraw coin
        """
        :param params:
         contains three parameters
         1 currency ex EAC
         2 quantity
         3 address(EAC Address)
         withdraw(currency='EAC',quantity=20.40,address="EAC_ADDRESS")
        """
        if self.key and self.secret:
            url = self.BASE_URL + "/payment/out/coin?currency=" + currency + '?' + self.key + '&nonce=' + str(
                int(time.time())) + urlencode(params)
            encoded_data = urllib.urlencode(params)
            sign = hmac.new(self.secret, msg=encoded_data, digestmod=hashlib.sha256).hexdigest().upper()
            headers = {"Api-key": self.key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}
            data = json.loads(requests.post(url, headers=headers).text)
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_order_book(self):
        ret = requests.get(self.BASE_URL + "exchange/order_book?currencyPair=" + self.current_pair,
                           headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return json.loads(data)

    # def get_all_order_book(self):
    #     ret = requests.get(self.BASE_URL + "exchange/all/order_book", headers={'User-Agent': 'Mozilla/5.0'})
    #     data = ret.text
    #     self.logger.info(self._format_log(data, "INFO"))
    #     return json.loads(data)

    def last_trade(self, currency_pair):
        ret = requests.get(self.BASE_URL + "exchange/last_trades?currencyPair=" + currency_pair,
                           headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return json.loads(data)

    def get_all_summary(self):
        ret = requests.get(self.BASE_URL + 'exchange/ticker', headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return json.loads(data)

    def get_summary(self):  # ticker data
        ret = requests.get(self.BASE_URL + "exchange/ticker?currencyPair=" + self.current_pair,
                           headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return self._parse_summary(json.loads(data))

    def get_maxbid_minask(self):
        ret = requests.get(self.BASE_URL + "exchange/maxbid_minask?currencyPair=" + self.current_pair,
                           headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return self._parse_summary(json.loads(data))


        #
        # def _get_continuous_ask_bid_prices(self):
        #     count = 0
        #     while self.is_continuous:
        #         self.summary = self.get_summary(self.current_pair)
        #         count += 1
        #         time.sleep(.1)
        #     print("Total hit for summary {}".format(count))
        #
        # def start_continuous_ask_bid_prices(self):
        #     self.is_continuous = True
        #     threading.Thread(target=self._get_continuous_ask_bid_prices).start()
        #
        # def stop_continuous_ask_bid_prices(self):
        #     # to stop execution of continuous order call this function
        #     self.is_continuous = False

        # def filterBTC(self):
        #     self.currency_list = filter(lambda currency_list: currency_list["MarketName"].find('BTC') > -1,
        #                                 self.currency_list)
        #     # self.currency_list = filter(lambda currency_list: currency_list["MarketName"]=='BTC-TKN', self.currency_list)

        # def startBetting(self):
        #     print("Betting Start")
        #     for i in range(len(self.currency_list)):
        #         price = 1 / self.currency_list[i]['Ask']
        #         self.currency_list[i].update({"hold": price})
        #         self.currency_list[i].update({"price": self.currency_list[i]['Ask']})
        #         self.currency_list[i].update({"ratio": 0})
        #     f = file('currency_list.dump', 'w')
        #     pickle.dump(self.currency_list, f)
        #     f.close()
        #
        # # def pickleLoad(self):
        #     from __builtin__ import file
        #     g = file('currency_list.dump', 'r')
        #     self.currency_list = pickle.load(g)

        # def sellBitcoin(self):
        #     if self.currency_list[0].has_key('hold'):
        #         for i in range(len(self.currency_list)):
        #
        #             if self.currency_list[i]['ratio'] > 10:
        #                 can_be_sold_ammount = ((self.currency_list[i]['hold']) - (1 / self.currency_list[i]['Bid']))
        #                 bitcoin_sold = can_be_sold_ammount * self.currency_list[i]['Bid']
        #                 # sell here
        #                 self.currency_list[i]['hold'] = self.currency_list[i]['hold'] - can_be_sold_ammount
        #                 self.currency_list[i]['price'] = 1 / self.currency_list[i]['hold']
        #                 if self.currency_list[i].has_key('sold'):
        #                     self.currency_list[i]['sold'] = self.currency_list[i]['sold'] + bitcoin_sold
        #                     self.currency_list[i]['sold_times'] = self.currency_list[i]['sold_times'] + 1
        #                 else:
        #                     self.currency_list[i].update({'sold': bitcoin_sold})
        #                     self.currency_list[i].update({'sold_times': 1})
        #
        #         f = file('currency_list.dump', 'w')
        #         pickle.dump(self.currency_list, f)
        #         f.close()

        # def debug(self):
        #     for i in range(len(self.currency_list)):
        #         self.currency_list[i]['debug_value'] = self.currency_list[i]['Ask'] * 1.2
        #
        # def printCoins(self):
        #     _currency_list = filter(lambda currency_list: currency_list["MarketName"].find('BTC') > -1, self.currency_list)[
        #                      0:10]
        #     print("==============")
        #     for currency in _currency_list:
        #         print("Bid: " + "%.10f" % currency['Bid'], )
        #         print("Ask: " + "%.10f" % currency['Ask'], )
        #         print("MarketName: " + currency['MarketName'], )
        #         if (currency.has_key('hold')):
        #             print("Hold: " + "%.10f" % currency['hold'], )
        #             print("Price: " + "%.10f" % currency['price'], )
        #             print("Ratio: " + str(round(currency['ratio'], 2)) + " %", )
        #         if (currency.has_key('sold')):
        #             print(" -------------- > ***** " + str(currency['sold_times']) + " times Sold: " + "%.10f" % currency[
        #                 'sold'] + "******", )
        #
        #         print('\n', )
        #     print("==============")


if __name__ == "__main__":
    lcoin = Livecoin()
    print(lcoin.get_order_book())
    print(lcoin.get_balance())
    # b = Bittrex(key="key", secret="secret")
    # print(b.get_summary())
    # thread.start_new_thread(bitLoop, ())
    #
    #
    # while 1:
    #     c = sys.stdin.read(1)
    #     if c == 'q':
    #         sys.exit()
    #     elif c == 's':
    #         b.bet_started = True
    #     elif c == 'l':
    #         b.pickleLoad()
    #     elif c == 'g':
    #         b.sellBitcoin()
    #     elif c == 'd':
    #         b.debug()
