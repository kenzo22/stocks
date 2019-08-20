
from jqdatasdk import *
auth('18621061452','061452')

print(__version__)

count=get_query_count()
print(count)
# {'total': 1000000,'spare': 996927}

#获取沪深300成分股
stocks = get_index_stocks('000300.XSHG')
print(stocks)

#获取某一天的上证指数的成份股权重
df = get_index_weights(index_id="000001.XSHG", date="2019-08-20")
print(df)
