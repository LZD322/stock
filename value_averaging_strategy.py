import backtrader as bt

# 定义默认的全局变量
default_date_tracker = []
default_invested_tracker = []
default_market_value_tracker = []


class ValueAveragingStrategy(bt.Strategy):
    params = (
        ('initial_investment', 0),  # 初始金额
        ('growth_rate', 0.01),  # 每月市值增长速度1%
        ('investment_amount', 10000),  # 每月固定定投金额
        ('date_tracker', default_date_tracker),  # 全局日期追踪器
        ('invested_tracker', default_invested_tracker),  # 全局投资追踪器
        ('market_value_tracker', default_market_value_tracker)  # 全局市值追踪器
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.current_value = 0  # 当前持仓市值
        self.target_value = self.params.initial_investment  # 初始目标市值
        self.months_for_va = [2, 5, 8, 11]  # 进行价值平均的月份
        self.total_invested = 0  # 记录累计使用的资金

        # 初始化全局变量
        self.date_tracker = self.params.date_tracker
        self.invested_tracker = self.params.invested_tracker
        self.market_value_tracker = self.params.market_value_tracker

    def next(self):
        current_date = self.datas[0].datetime.date(0)
        current_month = current_date.month
        current_day = current_date.day

        if current_day > 10:
            if hasattr(self, 'already_executed') and self.already_executed.get(current_month, False):
                return
            self.already_executed = {current_month: True}

            if self.position:
                self.current_value = self.position.size * self.dataclose[0]
            else:
                self.current_value = 0

            # 目标市值，按每月1%的增长
            self.target_value = self.target_value * (1 + self.params.growth_rate) + self.params.investment_amount

            print("\n")
            print("当前日期：", current_date)
            print("当前点位：", self.dataclose[0])
            print("当前份数：", self.position.size)
            print("当前市值：", self.current_value)
            print(f"累计投入资金：{self.total_invested:.2f}")
            print(f"当前收益：{self.current_value - self.total_invested:.2f}")
            print("目标市值：", self.target_value)

            if current_month in self.months_for_va:
                difference = self.target_value - self.current_value
                if difference > 0:
                    amount_to_invest = difference / self.dataclose[0]
                    self.buy(size=amount_to_invest)
                    print("买入", amount_to_invest, "份")
                elif difference < 0:
                    amount_to_sell = abs(difference) / self.dataclose[0]
                    self.sell(size=amount_to_sell)
                    print("卖出", amount_to_sell, "份")

                self.total_invested += difference
            else:
                amount_to_invest = self.params.investment_amount / self.dataclose[0]
                self.buy(size=amount_to_invest)
                self.total_invested += self.params.investment_amount
                print("买入", amount_to_invest, "份")

        # 更新全局列表
        self.date_tracker.append(current_date)
        self.invested_tracker.append(self.total_invested)
        self.market_value_tracker.append(self.position.size * self.dataclose[0])

    def stop(self):
        # 计算最终的市值
        self.final_value = self.position.size * self.dataclose[0] if self.position else 0

        # 计算收益率
        profit = self.final_value - self.total_invested
        roi = (profit / self.total_invested) * 100 if self.total_invested != 0 else 0

        # 获取最终日期
        final_date = self.datas[0].datetime.date(0)

        # 将最终日期、累计投入资金和最终市值更新到追踪数组中
        self.date_tracker.append(final_date)
        self.invested_tracker.append(self.total_invested)
        self.market_value_tracker.append(self.final_value)

        print("\n回测结束")
        print(f"累计投入资金：{self.total_invested:.2f}")
        print(f"最终持仓市值：{self.final_value:.2f}")
        print(f"绝对收益：{self.final_value - self.total_invested:.2f}")
        print(f"收益率：{roi:.2f}%\n")



