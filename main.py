# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.
from back_testing import value_averaging_back_testing


if __name__ == '__main__':
    value_averaging_back_testing('C:\\Users\\lizhe\\Desktop\\指数数据\\沪深300-20040104-20240930.csv',
                                 start_date='2005-01-01',
                                 end_date='2024-12-31',
                                 initial_investment=0,
                                 growth_rate=0.01,
                                 investment_amount=10000)






