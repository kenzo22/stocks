
from jqdatasdk import *
auth('18621061452','061452')

print(__version__)

count=get_query_count()
print(count)
# {'total': 1000000,'spare': 996927}

# # 获取沪深300成分股
# stocks = get_index_stocks('000300.XSHG')
# print(stocks)

# #获取某一天的上证指数的成份股权重
# df = get_index_weights(index_id="000001.XSHG", date="2019-08-20")
# print(df)

#将所有股票列表转换成数组
stocks = list(get_all_securities(['stock']).index)
print(list)

# #获得所有指数列表
# get_all_securities(['index'])
#
# #获得所有基金列表
# df = get_all_securities(['fund'])
#
# #获取所有期货列表
# get_all_securities(['futures'])
#
# #获得etf基金列表
# df = get_all_securities(['etf'])
# #获得lof基金列表
# df = get_all_securities(['lof'])
# #获得分级A基金列表
# df = get_all_securities(['fja'])
# #获得分级B基金列表
# df = get_all_securities(['fjb'])
#
# #获得2015年10月10日还在上市的所有股票列表
# get_all_securities(date='2015-10-10')
# #获得2015年10月10日还在上市的 etf 和 lof 基金列表
# get_all_securities(['etf', 'lof'], '2015-10-10')

# 查询最近10个交易日申万一级行业指数-农林牧渔行业（801010）的日行情数据。
df=finance.run_query(query(finance.SW1_DAILY_PRICE).filter(finance.SW1_DAILY_PRICE.code=='801010').order_by(finance.SW1_DAILY_PRICE.date.desc()).limit(10))
print(df)

# 查询最近10个交易日申万一级行业指数-农林牧渔行业（801010）的估值数据
df=finance.run_query(query(finance.SW1_DAILY_VALUATION).filter(finance.SW1_DAILY_VALUATION.code=='801010').order_by(finance.SW1_DAILY_VALUATION.date.desc()).limit(10))
print(df)

# 获取一支股票
df = get_price('000001.XSHE') # 获取000001.XSHE的2015年的按天数据
df = get_price('000001.XSHE', start_date='2015-01-01', end_date='2015-01-31 23:00:00', frequency='minute', fields=['open', 'close']) # 获得000001.XSHG的2015年01月的分钟数据, 只获取open+close字段
df = get_price('000001.XSHE', count = 2, end_date='2015-01-31', frequency='daily', fields=['open', 'close']) # 获取获得000001.XSHG在2015年01月31日前2个交易日的数据
df = get_price('000001.XSHE', start_date='2015-12-01 14:00:00', end_date='2015-12-02 12:00:00', frequency='1m') # 获得000001.XSHG的2015年12月1号14:00-2015年12月2日12:00的分钟数据

# 获取多只股票
panel =  get_price(get_index_stocks('000903.XSHG')) # 获取中证100的所有成分股的2015年的天数据, 返回一个[pandas.Panel]
df_open = panel['open']  # 获取开盘价的[pandas.DataFrame],  行索引是[datetime.datetime]对象, 列索引是股票代号
df_volume = panel['volume']  # 获取交易量的[pandas.DataFrame]

df_open['000001.XSHE'] # 获取平安银行的2015年每天的开盘价数据

# 在交易时间段获取当前实时分钟数据
# 交易所没有提供分钟级别数据，分钟数据需要再次处理，获取实时行情数据时，为了可以保证获取当前分钟的数据，请在第10秒后获取分钟数据
import datetime as dt
stocks = ['000001.XSHE', '600000.XSHG']
# 获取当前时间
now = dt.datetime.now()
print("当前时间为 {0}".format(now))
# 获取当前秒数
second = now.second

# 判断当前秒数是否大于10
if second >= 10:
    # 获取多只股票当前一条分钟数据
    df1 = get_price(stocks, end_date=now, count=1, frequency='1m')
    print(df1['close'])

    # 获取截至当前时间，当天的历史分钟数据
    today = now.strftime('%Y-%m-%d')
    df2 = get_price(stocks, start_date=today + ' 09:00:00', end_date=now, frequency='1m')
    print(df2['close'])
else:
    print("当前秒数为{0},小于10,请稍后再获取当前分钟数据".format(second))




# 获取一只股票在一个时间段内的资金流量数据
get_money_flow('000001.XSHE', '2016-02-01', '2016-02-04')
get_money_flow('000001.XSHE', '2015-10-01', '2015-12-30', field="change_pct")
get_money_flow(['000001.XSHE'], '2010-01-01', '2010-01-30', ["date", "sec_code", "change_pct", "net_amount_main", "net_pct_l", "net_amount_m"])

# 获取多只股票在一个时间段内的资金流向数据
get_money_flow(['000001.XSHE', '000040.XSHE', '000099.XSHE'], '2010-01-01', '2010-01-30')
# 获取多只股票在某一天的资金流向数据
get_money_flow(['000001.XSHE', '000040.XSHE', '000099.XSHE'], '2016-04-01', '2016-04-01')


# 获取2018-08-01的龙虎榜数据
get_billboard_list(stock_list=None, end_date = '2018-08-01', count =1)
