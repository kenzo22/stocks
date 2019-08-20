#coding=utf-8

import tushare  as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error

df = ts.get_hist_data('000001',start='2019-01-01',end='2019-08-20')

sz=df.sort_index(axis=0, ascending=True) #对index进行升序排列，按行进行排序
sz_return=sz[['p_change']] #选取涨跌幅数据，选取的是dataframe
train=sz_return[0:120] #划分训练集
test=sz_return[120:]   #测试集
#对训练集与测试集分别做趋势图
plt.figure(figsize=(10,5))
train['p_change'].plot()
plt.legend(loc='best')
plt.show()
plt.figure(figsize=(10,5))
test['p_change'].plot(c='r')
plt.legend(loc='best')
plt.show()

# #Simple Average
# y_hat_avg = test.copy() #copy test列表
# y_hat_avg['avg_forecast'] = train['p_change'].mean() #求平均值
# plt.figure(figsize=(12,8))
# plt.plot(train['p_change'], label='Train')
# plt.plot(test['p_change'], label='Test')
# plt.plot(y_hat_avg['avg_forecast'], label='Average Forecast')
# plt.legend(loc='best')
# plt.show()
# rms = sqrt(mean_squared_error(test.p_change, y_hat_avg.avg_forecast))
# print(rms)

#Moving Average
y_hat_avg = test.copy()
y_hat_avg['moving_avg_forecast'] = train['p_change'].rolling(30).mean().iloc[-1]
#30期的移动平均，最后一个数作为test的预测值
plt.figure(figsize=(12,8))
plt.plot(train['p_change'], label='Train')
plt.plot(test['p_change'], label='Test')
plt.plot(y_hat_avg['moving_avg_forecast'], label='Moving Average Forecast')
plt.legend(loc='best')
plt.show()
rms = sqrt(mean_squared_error(test.p_change, y_hat_avg.moving_avg_forecast))
print(rms)
