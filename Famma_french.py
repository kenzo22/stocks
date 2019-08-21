import numpy as np
import pandas as pd

def init(context):
    update_universe('600000.XSHG')
    context.first_shot = True
    #context.benchmark = '600000.XSHG'
# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新

def before_trading(context):
    #策略开始时初始化时间记录，股票列表，记录价格，市值，bookvalue的Series，
    if context.first_shot :
        context.first_shot = False
        context.current_month = context.now.month

        #股票池选取
        dp = get_fundamentals(
                    query(fundamentals.eod_derivative_indicator.market_cap)
                    )
        context.stocks = list(dp.columns)

        #context.stocks.remove('600553.XSHG')
        #context.stocks.remove('000578.XSHE')
        #context.stocks.remove('600631.XSHG')
        context.stocks.remove('000787.XSHE')
        context.stocks.remove('000805.XSHE')
        context.stocks.remove('000522.XSHE')
        context.stocks.remove('000602.XSHE')
        context.stocks.remove('000527.XSHE')
        context.stocks.remove('000562.XSHE')
        to_be_removed=[]
        for stk in context.stocks:
            if stk[10]=='G':
                to_be_removed.append(stk)
        for stk in to_be_removed:
            context.stocks.remove(stk)

        context.stocks.append('600000.XSHG')

        context.current_price = pd.Series(index = context.stocks)
        context.last_price = pd.Series(index = context.stocks)
        context.mktc = pd.Series(index = context.stocks)
        context.bps = pd.Series(index = context.stocks)

        for stk in context.stocks:
            context.last_price[stk] = history(1,'1d','last')[stk][0]

            if context.last_price[stk]==np.nan:
                context.last_price[stk] = 0

        #记录市场回报的价格
        context.last_mkt_price = history(1,'1d','last')['000300.XSHG'][0]

    #当月份更新时，记录现在的价格和市值bookvalue，以计算smb，hmi，Return
    if  context.current_month != context.now.month:
        #清空Series

        context.mktc = pd.Series(index = context.stocks)
        context.bps = pd.Series(index = context.stocks)
        context.current_price = pd.Series(index = context.stocks)

        for stk in context.stocks:
            context.current_price[stk] = history(1,'1d','last')[stk][0]
        context.current_mkt_price = history(1,'1d','last')['000300.XSHG'][0]
        for stk in context.stocks:
            dp = get_fundamentals(
                    query(fundamentals.eod_derivative_indicator.market_cap,fundamentals.financial_indicator.book_value_per_share)
                    .filter(fundamentals.eod_derivative_indicator.stockcode == stk))
            context.mktc[stk] = dp[stk]['market_cap']
            context.bps[stk] = dp[stk]['book_value_per_share']

def handle_bar(context, bar_dict):
    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息
    # 使用order_shares(id_or_ins, amount)方法进行落单！

    if context.current_month==context.now.month:
        return
    else:
        context.current_month = context.now.month
        #调整nan值
        where_are_NaNs = np.isnan(context.bps)
        context.bps[where_are_NaNs] = 0
        where_are_NaNs = np.isnan(context.mktc)
        context.mktc[where_are_NaNs] = 0
        for stk in context.stocks:
            if context.current_price[stk]==np.nan:
                context.current_price[stk] = 0
            if context.last_price[stk]==np.nan:
                context.last_price[stk] = 0

        #calculate book to market ratio
        btm = pd.Series(index=context.stocks)
        for stk in context.stocks:
            if context.current_price[stk]!=0:
                btm[stk] = context.bps[stk] / context.current_price[stk]
            else:
                btm[stk] = 0

        ##calculate market size medians
        median_size = np.median(context.mktc)
        ##calculate the 30%, 70% quantile of book to market ratio
        smark = np.percentile(list(btm),30)
        hmark = np.percentile(list(btm),70)
        if smark == 0:
            smark=hmark/2

        return_data = pd.Series(index=context.stocks)
        for stk in context.stocks:
            if context.current_price[stk]==0:
                return_data[stk] = 0
            else:
                return_data[stk] = context.current_price[stk]/context.last_price[stk] - 1

        small_size=0.0
        big_size=0.0
        value_btm=0.0
        growth_btm=0.0
        for stk in context.stocks:
            if context.mktc[stk]<median_size:
                small_size = small_size + return_data[stk] * context.mktc[stk]
            else:
                big_size = big_size + return_data[stk] * context.mktc[stk]
            if btm[stk] < smark:
                growth_btm = growth_btm + return_data[stk]*context.mktc[stk]
            elif btm[stk]>hmark:
                value_btm = value_btm + return_data[stk]*context.mktc[stk]

        mktcap = np.sum(context.mktc)
        smb = (small_size - big_size)/mktcap
        hmi = (value_btm - growth_btm)/mktcap

        Rm = context.current_mkt_price/context.last_mkt_price - 1-0.00375724091

        ref = (-0.0022684101268798463+0.16417514447020232*Rm - 0.97619263840653125*smb+0.2312581654106953*hmi+0.00375724091 + 1 ) * context.last_price['600000.XSHG']

        if bar_dict['600000.XSHG'].last < (ref*0.95):
            order_target_percent('600000.XSHG',1)
        if bar_dict['600000.XSHG'].last > (ref*1.05):
            order_target_percent('600000.XSHG',0)

        context.last_price = context.current_price
        context.last_mkt_price = context.current_mkt_price
