import tushare as ts
import pandas as pd
import datetime

ts.set_token('bd06cffbbcd6a06555a22e14e94b635b8c8b1c65ca0ec7d3c8d0cc07')
pro = ts.pro_api()

code_me = '000002.SZ, 002027.SZ,000681.SZ,600297.SH,002508.SZ,601318.SH,601633.SH,600383.SH,000858.SZ,601166.SH'
portfolio_me = pd.DataFrame({'name':["万科A", "分众传媒","视觉中国","广汇汽车","老板电器","中国平安","长城汽车","金地集团","兴业银行"],
'ts_code':["000002.SZ", "002027.SZ","000681.SZ","600297.SH","002508.SZ","601318.SH","601633.SH","600383.SH","601166.SH"]})

code_yuan = '000002.SZ,002027.SZ,000681.SZ,600036.SH,600297.SH,300383.SZ,002508.SZ,601318.SH,601633.SH,600383.SH,601601.SH,000858.SZ,002304.SZ,002727.SZ,601009.SH,600048.SH,600104.SH,601166.SH,601688.SH,300450.SZ,002475.SZ,300308.SZ,603833.SH,002410.SZ,600887.SH,601288.SH'
portfolio_yuan = pd.DataFrame({'name':["分众传媒","视觉中国","招商银行","广汇汽车","中国平安","长城汽车","中国太保","洋河股份","一心堂","南京银行","保利地产","上汽集团","华泰证券","农业银行"],
'ts_code':["002027.SZ","000681.SZ","600036.SH","600297.SH","601318.SH","601633.SH","601601.SH","002304.SZ","002727.SZ","601009.SH","600048.SH","600104.SH","601688.SH","601288.SH"]})

code_all = '000002.SZ,002027.SZ,000681.SZ,600036.SH,600297.SH,300383.SZ,002508.SZ,601318.SH,601633.SH,600383.SH,601601.SH,000858.SZ,002304.SZ,002727.SZ,601009.SH,600048.SH,600104.SH,601166.SH,601688.SH,300450.SZ,002475.SZ,300308.SZ,603833.SH,002410.SZ,600887.SH'
portfolio_all = pd.DataFrame({'name':["万科A", "分众传媒","视觉中国","招商银行","广汇汽车","光环新网","老板电器","中国平安","长城汽车","金地集团","中国太保","五粮液","洋河股份","一心堂","南京银行","保利地产","上汽集团","兴业银行","华泰证券","先导智能","立讯精密","中际旭创","欧派家居","广联达","伊利股份"],
'ts_code':["000002.SZ", "002027.SZ","000681.SZ","600036.SH","600297.SH","300383.SZ","002508.SZ","601318.SH","601633.SH","600383.SH","601601.SH","000858.SZ","002304.SZ","002727.SZ","601009.SH","600048.SH","600104.SH","601166.SH","601688.SH","300450.SZ","002475.SZ","300308.SZ","603833.SH","002410.SZ","600887.SH"]})

today = datetime.date.today().strftime('%Y%m%d')
yesterday = (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y%m%d')

def getStockPrice(code, portfolio, date):
    close_price = pro.daily(ts_code=code, start_date=date, end_date=date)[['ts_code','close']]
    result = pd.merge(portfolio, close_price, on = 'ts_code')[['close']]
    result.to_csv('./stock.csv', index = False)
    print(result)

# getStockPrice(code_me,portfolio_me,today)
# getStockPrice(code_me,portfolio_me,yesterday)
# getStockPrice(code_yuan,portfolio_yuan,today)
# getStockPrice(code_yuan,portfolio_yuan,yesterday)
getStockPrice(code_all,portfolio_all,today)
# getStockPrice(code_all,portfolio_all,yesterday)
