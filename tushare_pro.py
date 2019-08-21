import tushare as ts

pro = ts.pro_api('8e497aa2e327fb8694f9bc5f8b2f1a97f08fe66e6fd50a1857eb3066')

df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')

#df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
print(df)
