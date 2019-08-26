from jqdatasdk import *
auth('18621061452','061452')

# 查询'000001.XSHE'的所有市值数据, 时间是2015-10-15
q = query(
    valuation
).filter(
    valuation.code == '000001.XSHE'
)
df = get_fundamentals(q, '2015-10-15')
# 打印出总市值
print(df['market_cap'][0])

# 获取多只股票在某一日期的市值, 利润
df = get_fundamentals(query(
        valuation, income
    ).filter(
        # 这里不能使用 in 操作, 要使用in_()函数
        valuation.code.in_(['000001.XSHE', '600000.XSHG'])
    ), date='2015-10-15')

# 选出所有的总市值大于1000亿元, 市盈率小于10, 营业总收入大于200亿元的股票
df = get_fundamentals(query(
        valuation.code, valuation.market_cap, valuation.pe_ratio, income.total_operating_revenue
    ).filter(
        valuation.market_cap > 1000,
        valuation.pe_ratio < 10,
        income.total_operating_revenue > 2e10
    ).order_by(
        # 按市值降序排列
        valuation.market_cap.desc()
    ).limit(
        # 最多返回100个
        100
    ), date='2015-10-15')


from sqlalchemy.sql.expression import or_
get_fundamentals(query(
        valuation.code
    ).filter(
        or_(
            valuation.market_cap > 1000,
            valuation.pe_ratio < 10
        )
    ))


# 查询平安银行2014年四个季度的季报, 放到数组中
q = query(
        income.statDate,
        income.code,
        income.basic_eps,
        balance.cash_equivalents,
        cash_flow.goods_sale_and_service_render_cash
    ).filter(
        income.code == '000001.XSHE',
    )

rets = [get_fundamentals(q, statDate='2014q'+str(i)) for i in range(1, 5)]

# 查询平安银行2014年的年报
q = query(
        income.statDate,
        income.code,
        income.basic_eps,
        cash_flow.goods_sale_and_service_render_cash
    ).filter(
        income.code == '000001.XSHE',
    )

ret = get_fundamentals(q, statDate='2014')
