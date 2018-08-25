import json


from client.binance import BinanceClient
from client.gateio import GateioClient


ba = BinanceClient()
gate = GateioClient()
ba_result = ba.fetch_tickers()['data']
gate_result = gate.fetch_tickers()['data']

print(len(ba_result))
print(len(gate_result))

same_pair = ba_result.keys() & gate_result.keys()
row_same = {key: gate_result[key] for key in same_pair}
sorted_same = zip(row_same.values(), row_same.keys())
sorted_same = sorted(sorted_same, reverse=True)
for item in sorted_same:
    if item[0] < 150000:
        sorted_same.remove(item)
print(len(sorted_same))
result = json.dumps(sorted_same)
print(result)
with open('../logs/biance_gateio_same_pair', 'a', encoding='utf-8') as file:
    file.write(result)
    file.write(f'\n总共：{len(sorted_same)} 对每日交易量大于15w的交易对')
    file.close()
