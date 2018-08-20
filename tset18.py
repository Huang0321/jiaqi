import re
import time

import ccxt
import gevent

from gevent import monkey; monkey.patch_all()

from utils import logger


def fetch_order_book(client, pair):
    """获取order_book信息"""
    try:
        result = {}
        resp = client.fetch_order_book(pair, limit=5)
        result['ask1_price'] = resp['asks'][0][0]
        result['bid1_price'] = resp['bids'][0][0]
        result['pair'] = pair
        result['status'] = 0
        return result
    except Exception as e:
        logger.error(e)
        return {'status': -1, 'errmsg': 'request_failed'}


def judge_price(a_value, b_value, a_ask_price1, a_bid1_price, b_ask1_price, b_bid1_price, count):
    if a_value['status'] == 0 and b_value['status'] == 0:
        if a_value['ask1_price'] == a_ask_price1 and a_value['bid1_price'] == a_bid1_price and \
            b_value['ask1_price'] == b_ask1_price and b_value['bid1_price'] == b_bid1_price:
            return {"status": -1, 'msg': 'Order_book has not change yet'}
        else:
            a = (a_value['bid1_price'] - b_value['ask1_price']) / a_value['bid1_price']
            b = (b_value['bid1_price'] - a_value['ask1_price']) / b_value['bid1_price']
           if a > 0.0035:
                count[0] += 1
                logger.info("name = {}; a = {}; b= {}; count = {}".format(a_value['pair'], a, b, count[0]))
                logger.info('a: %s; b: %s' % (a_value, b_value))
                logger.critical('{} Generate transaction signal: {} {}'.format(a_value["pair"], a_value, b_value))
                return {'status': 0}
            elif b > 0.0035:
                count[1] += 1
                logger.info("name = {}; a = {}; b= {}; count = {}".format(a_value['pair'], a, b, count[1]))
                logger.info('a: %s; b: %s' % (a_value, b_value))
                logger.critical('{} Generate transaction signal: {} {}'.format(a_value["pair"], a_value, b_value))
                return {'status': 0}
           else:
                return {'status': -1, 'msg': 'No signal'}
    else:
        return {'status':-1, 'errmsg': 'fetch_book_error'}


def main():
    okex = ccxt.okex()
    bittrex = ccxt.bittrex()

    # temp = re.compile('{(.*)}')

    # with open("okex_bittrex_same_tarde_pair.log", 'r', encoding='utf-8') as sam_pair:
      #  info = sam_pair.readline()

   #  math_str = temp.search(info)

   #  same_pair_str = math_str.group(1)

   # same_pair_str = same_pair_str.replace("'", '')
    # same_pair_str = same_pair_str.replace(" ", '')
    # same_pair_list = same_pair_str.split(',')

    # 创造记录上一次价格的变量，以便盘口信息没有变动，但是一直判断有交易信号
    a_ask1_price = 0
    a_bid1_price = 0
    b_ask1_price = 0
    b_bid1_price = 0
    c_ask1_price = 0
    c_bid1_price = 0
    d_ask1_price = 0
    d_bid1_price = 0
    e_ask1_price = 0
    e_bid1_price = 0
    f_ask1_price = 0
    f_bid1_price = 0

    # 计数产生交易信号的次数， 初始为0
    count1 = [0, 0]
    count2 = [0, 0]
    count3 = [0, 0]

    while True:
        time.sleep(0.5)
        try:
            tasks = [gevent.spawn(fetch_order_book, okex, 'TRX/USDT'),
                     gevent.spawn(fetch_order_book, okex, 'XLM/BTC'),
                     gevent.spawn(fetch_order_book, okex, 'NEO/BTC'),
                     gevent.spawn(fetch_order_book, bittrex, 'TRX/USDT'),
                     gevent.spawn(fetch_order_book, bittrex, 'XLM/BTC'),
                     gevent.spawn(fetch_order_book, bittrex, 'NEO/BTC')]
            gevent.joinall(tasks)
            task1, task2, task3, task4, task5, task6 = tasks
            # print(task1.value, task4.value)
            # print(task2.value, task5.value)
            # print(task3.value, task6.value)
        except Exception as e:
            logger.error(e)
        else:
            result1 = judge_price(task1.value, task4.value, a_ask1_price, a_bid1_price, d_ask1_price, d_bid1_price, count1)
            result2 = judge_price(task2.value, task5.value, b_ask1_price, b_bid1_price, e_ask1_price, e_bid1_price, count2)
            result3 = judge_price(task3.value, task6.value, c_ask1_price, c_bid1_price, f_ask1_price, f_bid1_price, count3)
            try:
                a_ask1_price, a_bid1_price = task1.value['ask1_price'], task1.value['bid1_price']
                b_ask1_price, b_bid1_price = task2.value['ask1_price'], task2.value['bid1_price']
                c_ask1_price, c_bid1_price = task3.value['ask1_price'], task3.value['bid1_price']
                d_ask1_price, d_bid1_price = task4.value['ask1_price'], task4.value['bid1_price']
                e_ask1_price, e_bid1_price = task5.value['ask1_price'], task5.value['bid1_price']
                f_ask1_price, f_bid1_price = task6.value['ask1_price'], task6.value['bid1_price']
                print('a_circle_end\n')
            except Exception as e:
                logger.error('e')
   

if __name__ == '__main__':
    main()









