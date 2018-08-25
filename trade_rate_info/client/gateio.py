import ccxt

from settings import KEY_SECRET, BTC_VALUE, USDT_VALUE, ETH_VALUE
from utils import logger


class GateioClient(object):

    def __init__(self):
        self.name = 'gateio'
        self.client = ccxt.gateio()
        self.client.apiKey = KEY_SECRET['gateio'][0]
        self.client.secret = KEY_SECRET['gateio'][1]

    def fetch_tickers(self):
        """
        获取交易对和数量
        :return: {
            'status': 0,
            'data': {
            'BTC/USDT': 11111}  #交易对每天交易的市值，单位:￥
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
            logger.error('ErrorCode 10202 %s' % e)
            return {'status': -1, 'errmsg': 'fetch_tickers_failed'}

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

