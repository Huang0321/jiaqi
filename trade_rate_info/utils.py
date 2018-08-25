import os
import logging


ch = logging.StreamHandler()

# 设置文件分类输出
# debug 级别 log 到 debug 文件
fh_debug = logging.FileHandler(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs'),
                                            'binance_gateio_trade_pair_info.log'))
fh_debug.setLevel(logging.DEBUG)

# info级别输出到info文件
# fh_info = logging.FileHandler('logs/logging_info.log')
# fh_info.setLevel(logging.INFO)

# error级别 log 到 error文件
# fh_error = logging.FileHandler('logs/logging_error.log')
# fh_error.setLevel(logging.ERROR)

# critical 级别记录到critical文件


def create_logger(level=logging.DEBUG, record_format=None):
    """Create a logger according to the given settings"""
    # if record_format is None:
    #     # record_format = "%(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s\t%(threadName)s\t%(message)s"
    #     record_format = "%(asctime)s\t%(levelname)s\t%(message)s"
    # 可以直接设置在基础配置中，也可以在具体使用时详细配置
    # logging.basicConfig(filename='new.log',
    #                     filemode='a')
    # 实例化一个logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level) # 可以直接输入'大写的名称'， 也可以直接用logging.level： logging.debug
    ch.setLevel(level)
    formatter = logging.Formatter(record_format)
    ch.setFormatter(formatter)
    fh_debug.setFormatter(formatter)
    # fh_debug.filter(logging.DEBUG)
    # fh_info.setFormatter(formatter)
    # fh_info.filter(logging.INFO)
    # fh_error.setFormatter(formatter)
    # fh_error.filter(logging.ERROR)
    logger.addHandler(fh_debug)
    # logger.addHandler(fh_info)
    # logger.addHandler(fh_error)
    logger.addHandler(ch)
    return logger


logger = create_logger()


