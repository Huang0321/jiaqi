import gevent

from settings import RATE_1, RATE_2
from utils import logger


def check_signal(client1, client2, symbol):
    print('check_signal')
    task1 = gevent.spawn(client1.fetch_order_book, symbol)
    task2 = gevent.spawn(client2.fetch_order_book, symbol)
    gevent.joinall([task1, task2])
    resp1 = task1.value
    resp2 = task2.value
    if resp1['status'] == 0 and resp2['status'] == 0:
        # 如果价差达到 规定的利率，就成交
        if (resp1['data']['bid1'] - resp2['data']['ask1']) / resp1['data']['bid1'] > RATE_1:
            check_balance(client1, client2, resp1, resp2, symbol)
        elif (resp2['data']['bid1'] - resp1['data']['ask1']) / resp2['data']['bid1'] > RATE_2:
            check_balance(client2, client1, resp2, resp1, symbol)
        else:
            return {'status': -1, 'errmsg': 'no_trade_signal'}
    else:
        return {'status': -1, 'errmsg': 'fetch_order_book_failed'}


def check_balance(client1, client2, data1, data2, symbol):
    logger.info('check_balace')
    coin1, coin2 = symbol.split('/')
    task1 = gevent.spawn(client1.fetch_symbol_balance, symbol)
    task2 = gevent.spawn(client2.fetch_symbol_balance, symbol)
    gevent.joinall([task1, task2])
    resp1 = task1.value
    resp2 = task2.value
    print(3 * resp1['data'][coin1]['total'] * data1['data']['bid1'])
    print(2 * resp1['data'][coin2]['total'])
    print(2 * resp2['data'][coin1]['total'] * data2['data']['ask1'])
    print(3 * resp2['data'][coin2]['total'])
    if (3 * resp1['data'][coin1]['total'] * data1['data']['bid1']) < (2 * resp1['data'][coin2]['total']) or \
            (2 * resp2['data'][coin1]['total'] * data2['data']['ask1']) > (3 * resp2['data'][coin2]['total']):
        logger.info('blance_is_not_satisfied')
        return {'status': -1, 'errmsg': 'balance_not_satisfied'}
    else:
        volume = int(resp2['data'][coin2]['free'] / data2['data']['ask1'])
        if volume > 0:
            amount = min(data1['data']['bid1_qty'], data2['data']['ask1_qty'],
                         resp1['data'][coin1]['free'], volume)
            make_order(client1, client2, amount, data1['data']['bid1'], data2['data']['ask1'], symbol)
        else:
            logger.info('volume_not_satisfy')


def make_order(client1, client2, amount, price1, price2, symbol):
    logger.info('make_order')
    task1 = gevent.spawn(client1.create_limit_sell_order, symbol, amount, price1)
    task2 = gevent.spawn(client2.create_limit_buy_order, symbol, amount, price2)
    gevent.joinall([task1, task2])
    resp1 = task1.value
    resp2 = task2.value
    logger.info('make_limit_order: %s %s' % (resp1, resp2))
    if resp1['status'] == 0 and resp2['status'] == 0:
        return {'status': 0, 'msg': 'make_limit_order_success'}
    else:
        return {'status': -1, 'msg': 'make_limit_order_failed'}
