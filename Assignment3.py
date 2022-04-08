'''
Name: DIAO Xingning
Student ID: 221040078
Assignment3
Markowitz Portfolio Model
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(r'D:\Coding\Assignment3')

# import data
sz50 = pd.read_csv('sz50.csv', index_col='trddy')
sz50.index = pd.to_datetime(sz50.index)
sz50 = sz50.dropna(axis=1)
sz50 = sz50.dropna(axis=0)

# portfolio from assignment2
stock_list = ['600436.SH', '600809.SH', '600900.SH', '601088.SH', '601857.SH',\
              '601633.SH', '600745.SH', '600519.SH', '600036.SH', '603501.SH']

# historical data
stock_price = sz50.loc[:, stock_list]
stock_train = stock_price.iloc[:195, :]
stock_test = stock_price.iloc[195:, :]

# 股票净值从1开始
daily_returns = pd.DataFrame()
daily_returns_test = pd.DataFrame()

daily_returns = np.log(stock_train/stock_train.shift(1))[:]
daily_returns_test = np.log(stock_test/stock_test.shift(1))[:]

daily_returns = daily_returns.dropna()
daily_returns_test = daily_returns_test.dropna()

# correlation_matrix
correlation_matrix = daily_returns.corr()
cov_matrix = daily_returns.cov()



