# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import datetime
import logging
import requests
import sys
import os.path

dir = os.path.dirname(os.path.abspath(__file__)) + "/"


class Okex(object):
    ETH_ADDRESS = ""
    BTC_ADDRESS = ""
    BTC_BALANCE = 0
    ETH_BALANCE = 0

    def __init__(self, key=None, secret=None):
        self.logger = logging.getLogger("Okex")
        self.BASE_URL = "https://www.okex.com/api/v1/"
        self.handler = logging.FileHandler(dir + 'logs/okex.log')
        self.is_continuous = False
        self.key = '0f9ddba1-ef08-480d-976f-60046ac69fd8'
        self.secret = '42647E7209279FA0D9A9386938897A1E'
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

    def create_sign(self, params = {}):
        sign = ''
        for key in sorted(params.keys()):
            sign += key + '=' + str(params[key]) + '&'
        data = sign + 'secret_key=' + self.secret
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()

    def send_bets(self, **params):  # place limit order
        """
        :param params:
         contains three parameters
        1 type : order type: limit order(buy/sell) market order(buy_market/sell_market)
        2 price : order price. For limit orders, the price must be between 0~1,000,000.
                    IMPORTANT: for market buy orders, the price is to total amount you want to buy,
                    and it must be higher than the current price of 0.01 BTC (minimum buying unit),
                    0.1 LTC or 0.01 ETH. For market sell orders, the price is not required
        3 amount : order quantity. Must be higher than 0.01 for BTC, 0.1 for LTC or 0.01 for ETH.
                    For market buy roders, the amount is not required
        """
        if self.key and self.secret:
            url = self.BASE_URL + 'trade.do'
            data = {'api_key': self.key,
                      'symbol': self.current_pair,
                      'type': params['type']
                    }
            if params['price']:
                data['price'] = params['price']
            if params['amount']:
                data['amount'] = params['amount']
            data['sign'] = self.create_sign(data)
            data = json.loads(requests.post(url, data=data).text)
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_balance(self):
        if self.key and self.secret:
            url = self.BASE_URL + 'userinfo.do'
            data = {'api_key': self.key,}
            data['sign'] = self.create_sign(data)
            data = json.loads(requests.post(url, data=data).text)
            if isinstance(data, dict) and data['result'] == True:
                self.BTC_BALANCE = data['info']['funds']['free']['btc']
                self.ETH_BALANCE = data['info']['funds']['free']['eth']
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_order(self, orderId):
        if self.key and self.secret:
            url = self.BASE_URL + 'order_info.do'
            data = {'api_key': self.key,
                    'symbol': self.current_pair,
                    'order_id': orderId
                    }
            data['sign'] = self.create_sign(data)
            data = json.loads(requests.post(url, data=data).text)
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_orders(self, **params):
        """
        :param params:
         contains two parameters
        1. type : query type: 0 for unfilled (open) orders, 1 for filled orders
        2. order_id : order ID (multiple orders are separated by ',', 50 orders at most are allowed per request)
        """
        if self.key and self.secret:
            url = self.BASE_URL + 'orders_info.do'
            data = {'api_key': self.key,
                    'symbol': self.current_pair,
                    'type': params['type'],
                    'order_id': params['order_id']
                    }
            data['sign'] = self.create_sign(data)
            data = json.loads(requests.post(url, data=data).text)
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_trades(self, **params):
        """
        :param params:
         contains three parameters
        1. status : query status: 0 for unfilled orders, 1 for filled orders
        2. current_page : current page number
        3. page_length : number of orders returned per page, maximum 200
        """
        if self.key and self.secret:
            url = self.BASE_URL + 'order_history.do'
            data = {'api_key': self.key,
                    'symbol': self.current_pair,
                    'status': params['status'],
                    'current_page': params['currentPage'],
                    'page_length': params['pageLength']
                    }
            data['sign'] = self.create_sign(data)
            data = json.loads(requests.post(url, data=data).text)
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def cancel_limit(self, **params):
        if self.key and self.secret:
            url = self.BASE_URL + 'cancel_order.do'
            data = {'api_key': self.key,
                    'symbol': self.current_pair,
                    'order_id': params['order_id']
                    }
            data['sign'] = self.create_sign(data)
            data = json.loads(requests.post(url, data=data).text)
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def send_coin(self, **params):  # Withdraw coin
        """
        :param params:
         contains four parameters
         1 chargefee : network transaction fee, For withdraws to another OKCoin address, chargefee can be 0
                        and the withdraw will be 0 confirmation as well
         2 trade_pwd : trade/admin password
         3 withdraw_address
         4 withdraw_amount
         5 target : withdraw address type. okcoin.cn:"okcn" okcoin.com:"okcom" okes.com："okex" outer address:"address"
         6 currency
        """
        if self.key and self.secret:
            url = self.BASE_URL + 'withdraw.do'
            data = {'api_key': self.key,
                    'symbol': params['currency'],
                    'chargefee': params['chargefee'],
                    'trade_pwd': params['trade_pwd'],
                    'withdraw_address': params['withdraw_address'],
                    'withdraw_amount': params['withdraw_amount'],
                    'target': params['target']
                    }
            data['sign'] = self.create_sign(data)
            data = json.loads(requests.post(url, data=data).text)
            self.logger.info(self._format_log(data, "INFO"))
            return data
        else:
            return "KEY AND SECRET NEEDED FOR BETTING"

    def get_order_book(self):
        url = self.BASE_URL + 'depth.do?symbol=' + str(self.current_pair)
        ret = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return json.loads(data)

    def last_trade(self):
        url = self.BASE_URL + 'trades.do?symbol=' + str(self.current_pair)
        ret = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return json.loads(data)

    def get_summary(self):  # ticker data
        url = self.BASE_URL + 'ticker.do?symbol=' + str(self.current_pair)
        ret = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = ret.text
        self.logger.info(self._format_log(data, "INFO"))
        return self._parse_summary(json.loads(data))

    def get_candlestick_data(self):
        url = self.BASE_URL + 'kline.do?symbol=' + str(self.current_pair) + '&type=1day'
        data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        self.logger.info(self._format_log(data.text, "INFO"))
        return json.loads(data.text)


if __name__ == "__main__":
    ok = Okex()
    # print(ok.get_summary())
    # print(ok.get_order_book())
    # print(ok.last_trade())
    # print(ok.get_candlestick_data())
    # print(ok.get_balance())
    # print(ok.get_order('1244123'))
    # print(ok.get_orders(type='0', order_id=''))
    # print(ok.get_trades(status='0', pageLength='1', currentPage='1'))
    # print(ok.cancel_limit(order_id='234765'))
    # print(ok.send_coin(chargefee='0', trade_pwd='werrewq', withdraw_address='1234tyjnbvsahgtre', withdraw_amount='1',
    #                    target='', currency='BTC'))
    # print(ok.send_bets(type='buy', price='0', amount='0'))
