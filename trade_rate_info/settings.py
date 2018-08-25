# import pymysql
#
#
# # 创建数据库连接对象
# connect = pymysql.connect(host='119.28.227.49',
#                           port=3306,
#                           user='admin',
#                           password='admin',
#                           db='trade_pair_data',
#                           cursorclass=pymysql.cursors.DictCursor)


# 配置api_key 和 api_secret
KEY_SECRET = {
    'okex': ('6a689877-06c6-48b3-a4e2-5ce3b5931cc4', '3028064C9FA41F4C97070E7681FA9888'),
    'bittrex': ('d92a7f5fa0ad45589eaa2b7e6eb73457', '2f44fcd470584dfcbb5b71b5ca34583c'),
    'binance': ('okDJSyV9RkWUcSQ12wtYIGiuaEIKPaC66xMkj7aYh4GdxLlHoxb4HqDcq0U2BHdD',
                'xlVpquPLMzezLLv7dAEMUgQnNwMbHROZkAfy0KUnpsSxAZwBuzR9t6t5vv6MiyfJ'),
    'gateio': ('BF53EE5C-B72C-4316-8D2F-AD39A2669666',
               '06ec666e31189fcd7773c4274284de467486f0419fc2170708f1d979d88b0ab2')
}


# 静态价格,便于计算交易市值, 单位：￥
BTC_VALUE = 43773
ETH_VALUE = 1916
USDT_VALUE = 6.86

SYMBOL = 'LTC/USDT'

# 设置交易正反向利差
RATE_1 = 0.0035
RATE_2 = 0.0035