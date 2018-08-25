import time

from ccxt import bittrex

from settings import KEY_SECRET, BTC_VALUE, USDT_VALUE, ETH_VALUE
from utils import logger


class BittrexClient(object):

    def __init__(self):
        self.name = 'bittrex'
        self.client = bittrex()
        self.client.apiKey = KEY_SECRET['bittrex'][0]
        self.client.secret = KEY_SECRET['bittrex'][1]

    def fetch_symbol_balance(self, symbol):
        """
        获取某一交易对的账户信息
        :param symbol: trade_pari
        :return: {'status': 0,
            'data': {
                'ETH': {'free': 35.5, 'used': 0.0, 'total': 35.5}  # 单个币种的账户信息
                'EOS': {'free': 601.46998612, 'used': 0.0, 'total': 601.46998612} # 单个币种的账户信息
                }
            }
        """
        try:
            # 获取货币的名字
            coin1, coin2 = symbol.split('/')
            resp = self.client.fetch_balance()
            print(resp)
            # 获取货币在账户中的信息
            coin1_blc = resp[coin1]
            coin2_blc = resp[coin2]
            result = {'status': 0,
                'data': {
                    coin1: coin1_blc,
                    coin2: coin2_blc
                    }
                }
            return result
        except Exception as e:
            logger.error('ErrorCode 10201 %s' % e)
            return {'status': -1, 'errmsg': '%s_fetch_balance_failed' % self.name}

    def fetch_order_book(self, symbol):
        """
        获取盘口信息
        :param symbol: trade_pair
        :return: {'status': 0,
                'data': {
                    'symbol': 'NEO/USDT',
                    'ask1': 16.48187171,   # float
                    'ask1_qty': 83.17,   # float
                    'bid1': 16.38187171,  # float
                    'bid1_qty': 93.17, float
                    'exchange': okex,  # 交易所名称
                }
            }
        """
        try:
            resp = self.client.fetch_order_book(symbol, 5)  # 盘口深度限制5条, 但是对于某个交易所接口可能没有效果
            result = {'status': 0,
                'data': {
                    'symbol': symbol,
                    'ask1': resp['asks'][0][0],
                    'ask1_qty': resp['asks'][0][1],
                    'bid1': resp['bids'][0][0],
                    'bid1_qty': resp['bids'][0][1],
                    'exchange': self.name
                }
            }
            return result
        except Exception as e:
            logger.error('ErrorCode 10204 e')
            return {'status': -1, 'errmsg': '%s_fetch_order_book_failed' % self.name}

    def fetch_tickers(self):
        """
        获取交易所除了 'BTC/USDT', 'ETH/USDT', 'ETH/BTC'交易对以外所有交易对的折算成人民币的每天交易量
        :return: {'status': 0,
            'data':{
            'EOS/USDT': 18737193,
            'NEO/BTC': 33791939,
            ...
            ...
            'LEC/USDT': 113733}
            }
        """
        try:
            result = {'status': 0, 'data': {}}
            resp = self.client.fetch_tickers()
            for key in resp:
                if key not in ['BTC/USDT', 'ETH/USDT', 'ETH/BTC']:
                    if isinstance(key, str):
                        if 'BTC' in key:
                            result['data'][key] = resp[key]['baseVolume'] * resp[key]['last'] * BTC_VALUE
                        elif 'ETH' in key:
                            result['data'][key] = resp[key]['baseVolume'] * resp[key]['last'] * ETH_VALUE
                        else:
                            result['data'][key] = resp[key]['baseVolume'] * resp[key]['last'] * USDT_VALUE
            return result
        except Exception as e:
            logger.error("ErrorCode 10202 %s" % e)
            return {'status': -1, 'errmsg': '%s_fetch_tickers_failed' % self.name}

    def create_limit_buy_order(self, symbol, amount, price):
        """
        创建限价买单
        :param symbol: trade_pair  #str
        :param amount: trade_volume  # float
        :param price: trade_price   # float
        :return: {'status': 0,
                      'data': {
                          'order_id': '77388782',  # order_id
                          'symbol': 'NEO/USDT',
                          'side': 'buy' or 'sell',
                          'timestamp': 1534929118000  # int 但是需要除以1000才是正常的timestamp
                      }}
        """
        try:
            resp = self.client.create_limit_buy_order(symbol, amount, price)
            result = {'status': 0,
                      'data': {
                          'order_id': resp['id'],
                          'symbol': symbol,
                          'side': resp['side'],
                          'timestamp': int(time.time() * 1000)
                      }}
            return resp
        except Exception as e:
            logger.error('ErrorCode 10301 %s' % e)
            return {'status': -1, 'errmsg': '%s_create_limit_buy_order_failed' % self.name}

    def create_limit_sell_order(self, symbol, amount, price):
        """
        创建限价买单
        :param symbol: trade_pair  #str
        :param amount: trade_volume  # float
        :param price: trade_price   # float
        :return: {'status': 0,
                      'data': {
                          'order_id': '77388782',  # order_id
                          'symbol': 'NEO/USDT',
                          'side': 'buy' or 'sell',
                          'timestamp': 1534929118000  # int 但是需要除以1000才是正常的timestamp
                      }}
        """
        try:
            resp = self.client.create_limit_sell_order(symbol, amount, price)
            result = {'status': 0,
                      'data': {
                          'order_id': resp['id'],
                          'symbol': symbol,
                          'side': resp['side'],
                          'timestamp': int(time.time() * 1000)
                      }}
            return resp
        except Exception as e:
            logger.error('ErrorCode 10301 %s' % e)
            return {'status': -1, 'errmsg': '%s_create_limit_sell_order_failed' % self.name}

    def fetch_order(self, id, symbol):
        """
        获取订单信息
        :param id: order_id
        :param symbol: trade_pair
        :return: {'status': 0,
            'data': {
                'order_id': '100911291',  # str
                'timestamp': 1534929118000,  # int 是实际timestamp的1000倍
                'side': 'buy' or 'sell',
                'price': 18.32, float
                'amount': 6, float
                'filled': 5.3, float
                'remaining': 0.7, float
                'cost': 109.92, float
                'status': resp['status']
            }}
        """
        try:
            resp = self.client.fetch_order(id, symbol)
            result = {'status': 0,
                      'data': {
                          'order_id': resp['id'],
                          'timestamp': resp['timestamp'],
                          'side': resp['side'],
                          'price': resp['price'],
                          'amount': resp['amount'],
                          'filled': resp['filled'],
                          'remaining': resp['remaining'],
                          'cost': resp['cost'],
                          'status': resp['status']
                      }}
            return result
        except Exception as e:
            logger.error('ErrorCode 10302 %s' % e)
            return {'status': -1, 'errmsg': '%s_fetch_order_info_failed' % self.name}

    # 重复退单会发生抛出错误
    def cancel_order(self, id, symbol):
        """
        退单
        :param id: order_id,  str
        :param symbol: trade_pair
        :return: {'status': 0,
                'data': {
                    'order_id': '651c6831-439e-4874-9f96-9308fa2583c2',  # str
                    'status': 'canceled',
                    'timestamp': int(time.time() * 1000)
                }
            }
        """
        try:
            resp = self.client.cancel_order(id, symbol)
            result = {'status': 0,
                'data': {
                    'order_id': id,
                    'status': resp['status'],
                    'timestamp': int(time.time() * 1000)
                }
            }
            return resp
        except Exception as e:
            logger.error('ErrorCode 10303 %s' % e)
            return {'status': -1, 'errmsg': '%s_cancel_order_failed' % self.name}

