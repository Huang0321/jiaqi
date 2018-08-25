import time
from gevent import monkey; monkey.patch_all()
import gevent

from client.binance import BinanceClient
from client.gateio import GateioClient
from utils import logger


def create_tasks(client_list, symbol_list, tasks):
    """
    用个gevent创建异步任务,获取交易所的每个币种的返回值
    :param client_list: 交易所客户端实例的列表
    :param symbol_list: 交易对列表
    :param tasks: 用来装gevent任务的空列表
    :return: tasks 装有gevent任务的列表，返回值在每个 task.value里面
    """
    for client in client_list:
        for symbol in symbol_list:
            tasks.append(gevent.spawn(client.fetch_order_book, symbol))
    gevent.joinall(tasks)
    return tasks


def is_same(data, value):
    if data.value['data']['ask1'] == value[0] and data.value['data']['bid1'] == value[1]:
        return True
    else:
        value[0] = data.value['data']['ask1']
        value[1] = data.value['data']['bid1']
        return False


def check_price(data1, data2, value1, value2):
    """
    数据表
    :param data1:
    :param data2:
    :return:
    """
    if data1.value['status'] == 0 and data2.value['status'] == 0:
        if is_same(data1, value1) and is_same(data2, value2):
            rate1 = (data1.value['data']['bid1'] - data2.value['data']['ask1'])/data1.value['data']['bid1']
            rate2 = (data2.value['data']['bid1'] - data1.value['data']['ask1'])/data2.value['data']['bid1']
            return (data1.value['data']['symbol'], rate1, rate2, int(time.time() * 1000))
        else:
            return None
    else:
        return None


def get_value(tasks, value1, value2):
    client1_tasks = tasks[:(len(tasks)//2)]
    client2_tasks = tasks[(len(tasks)//2):]
    result = map(check_price, client1_tasks, client2_tasks, value1, value2)
    return result


def main():
    ba = BinanceClient()
    gate = GateioClient()
    client_list = [ba, gate]
    symbol_list = ['EOS/USDT', 'ONT/USDT', 'ADA/USDT', 'EOS/ETH', 'XRP/USDT']
    # 设置参照值
    value1 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    value2 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    while True:
        tasks = create_tasks(client_list, symbol_list, [])
        result = get_value(tasks, value1, value2)
        for item in result:
            if item:
                logger.info('{} {} {} {}'.format(item[0], item[1], item[2], item[3]))
        time.sleep(0.5)


if __name__ == "__main__":
    main()
