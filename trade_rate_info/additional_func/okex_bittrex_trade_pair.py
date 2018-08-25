import json

from client import bittrex, okex

# ok_cli = okex.OkexClient()
# bitx = bittrex.BittrexClient()
#
#
# ok_result = ok_cli.fetch_tickers()['data']
# bi_result = bitx.fectch_tickers()['data']
#
# print(len(ok_result))
# print(len(bi_result))
# same_pair  = ok_result.keys() & bi_result.keys()
# row_same = {key: bi_result[key] for key in same_pair}
# sorted_same = zip(row_same.values(), row_same.keys())
# sorted_same = sorted(sorted_same, reverse=True)
# for item in sorted_same:
#     if item[0] < 150000:
#         sorted_same.remove(item)
#
# result = json.dumps(sorted_same)

with open('../logs/okex_bittrex_same_pair.txt', 'r') as file:
    content = file.read()
    file.close()

content = json.loads(content)
print(type(content))


