from jqdatasdk import *
auth('18621061452','061452')

#查询雪球所有股票按当日新增关注人数排名的前10只个股
df=finance.run_query(query(finance.STK_XUEQIU_PUBLIC).filter(finance.STK_XUEQIU_PUBLIC.day=='2018-12-04').order_by(finance.STK_XUEQIU_PUBLIC.new_follower.desc()).limit(10))
print(df)

#获取新闻联播文本数据
df=finance.run_query(query(finance.CCTV_NEWS).filter(finance.CCTV_NEWS.day=='2019-02-19').limit(10))
print(df)

#进一步获取新闻正文内容
print(df.iloc[2,3])

# 查询分地区农林牧渔业总产值表(季度累计) 的前10条数据
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER
    ).limit(10)
df = macro.run_query(q)

# 查询2014年的分地区农林牧渔业总产值表(年度)
q = query(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR
        ).filter(macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR.stat_year=='2014')
df = macro.run_query(q)
