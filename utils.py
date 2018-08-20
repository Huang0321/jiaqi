import logging

ch = logging.StreamHandler()
fh = logging.FileHandler('ok_bit_statistics.log')


def create_logger(level=logging.DEBUG, record_format=None):
    """Create a logger according to the given settings"""
    if record_format is None:
        record_format = "%(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s\t%(threadName)s\t%(message)s"
    # 可以直接设置在基础配置中，也可以在具体使用时详细配置
    # logging.basicConfig( filename='new.log',
    #                      filemode='a')
    logger = logging.getLogger(__name__)
    logger.setLevel(level) # 可以直接输入'大写的名称'， 也可以直接用logging.level： logging.debug

    fh.setLevel(level)
    ch.setLevel(level)

    formatter = logging.Formatter(record_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

logger = create_logger()