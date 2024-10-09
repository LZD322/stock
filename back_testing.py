import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt
from value_averaging_strategy import ValueAveragingStrategy

def value_averaging_back_testing(csv_file, start_date=None, end_date=None,
                                 initial_investment=0, growth_rate=0.01, investment_amount=10000):
    # 存储信息用来作图
    global_date_tracker = []
    global_invested_tracker = []
    global_market_value_tracker = []

    # 创建回测引擎
    cerebro = bt.Cerebro()

    # 加载 CSV 文件数据
    data = pd.read_csv(csv_file, index_col='trade_date', parse_dates=True)

    # 如果传入了日期区间，则通过 pandas 过滤数据
    if start_date is not None and end_date is not None:
        filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]
    else:
        filtered_data = data  # 如果未传入日期区间，使用全部数据

    # 添加数据到 Backtrader
    datafeed = bt.feeds.PandasData(dataname=filtered_data)
    cerebro.adddata(datafeed)

    # 添加策略
    cerebro.addstrategy(ValueAveragingStrategy,
                        initial_investment=initial_investment,
                        growth_rate=growth_rate,
                        investment_amount=investment_amount,
                        date_tracker=global_date_tracker,
                        invested_tracker=global_invested_tracker,
                        market_value_tracker=global_market_value_tracker)

    # 禁用资金管理限制，使得可买入无资金限制
    cerebro.broker.setcash(1000000000000000000000000000000000000000000000.0)  # 初始资金设定，但不限制总资金
    cerebro.broker.setcommission(commission=0.0)  # 取消交易佣金
    cerebro.broker.set_checksubmit(False)  # 取消资金检查

    # 运行策略
    cerebro.run()

    # 自定义绘制累计投入资金和市值
    # 设置中文字体为 'Microsoft YaHei'，并取消负号显示问题
    plt.rcParams['font.sans-serif'] = ['YouYuan']  # Show Chinese label
    plt.rcParams['axes.unicode_minus'] = False  # These two lines need to be set manually
    plt.figure(figsize=(10, 6))
    plt.plot(global_date_tracker, global_invested_tracker, label='investment')
    plt.plot(global_date_tracker, global_market_value_tracker, label='value')
    plt.legend()
    plt.title('investment vs value')
    plt.xlabel('time')
    plt.ylabel('amount')
    plt.grid(True)
    plt.show()
