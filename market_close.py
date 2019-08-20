import tushare as ts
import pandas as pd
import time
import datetime
import os

#retval = os.getcwd() 获取当前工作目录
# 指定自己要存放文件的绝对路径
os.chdir('/Users/zxx/github/stocks/data')
pd.set_option('expand_frame_repr', False) #不允许换行

# now_time = datetime.datetime.now().strftime('%Y%m%d')

# 从tushare获取指定日期
def get_today_all_ts(date):
    date_now = date

    # 先获得所有股票的收盘数据
    df_close = ts.get_today_all()

    # 获得所有股票的基本信息
    df_basics = ts.get_stock_basics()
    df_all = pd.merge(left=df_close, right=df_basics, on='name', how='outer')

    df_all['code'] = df_all['code'].astype(str) + ' '

    # 保存数据
    df_all.to_csv(str(date_now) + '_ts.csv', index=False, encoding='utf-8') #不保存行索引
    print('%s is downloaded.' % (str(date_now)))
    print(df_all)
    return df_all

# if __name__ == '__main__'的意思是：当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；
# 当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
if __name__ == '__main__':
    get_today_all_ts(date=datetime.datetime.now().strftime('%Y%m%d'))
