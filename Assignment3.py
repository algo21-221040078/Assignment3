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

# calculate daily returns
daily_returns = pd.DataFrame()
daily_returns_test = pd.DataFrame()

daily_returns = np.log(stock_train/stock_train.shift(1))[:]
daily_returns_test = np.log(stock_test/stock_test.shift(1))[:]

daily_returns = daily_returns.dropna()
daily_returns_test = daily_returns_test.dropna()

# correlation_matrix
correlation_matrix = daily_returns.corr()
cov_matrix = daily_returns.cov()
cov_matrix_annual = cov_matrix * 252

# montecarlo
n = 10000
random_portfolio = np.empty((n, 12))
np.random.seed(12)

for i in range(n):
    random10 = np.random.random(10)
    random_weight = random10/np.sum(random10)

    mean_return = daily_returns.mul(random_weight, axis=1).sum(axis=1).mean()
    annual_return = (1 + mean_return)**252-1

    # bodonglv
    random_volatility = np.sqrt(np.dot(random_weight.T,np.dot(cov_matrix_annual,random_weight)))

    random_portfolio[i][:10] = random_weight
    random_portfolio[i][10] = np.array(annual_return)
    random_portfolio[i][11] = random_volatility

RandomPortfolios = pd.DataFrame(random_portfolio)
RandomPortfolios.columns = [stock+'_weight' for stock in stock_list]+['Returns','Volatility']

# 绘制散点图
RandomPortfolios.plot('Volatility', 'Returns', kind='scatter', alpha=0.3)
plt.show()

# min variance
min_index = RandomPortfolios.Volatility.idxmin()

RandomPortfolios.plot('Volatility', 'Returns', kind='scatter', alpha=0.3)
x = RandomPortfolios.loc[min_index, 'Volatility']
y = RandomPortfolios.loc[min_index, 'Returns']
plt.scatter(x, y, color='red')

plt.text(np.round(x,4), np.round(y,4), (np.round(x,4), np.round(y,4)),ha='left',va='bottom',fontsize=10)
plt.show()
print(RandomPortfolios.iloc[min_index])

# test data set
optimal_portfolio = RandomPortfolios.iloc[min_index,:10]
optimal_portfolio = optimal_portfolio.to_list()
mean_return_test = daily_returns_test.mul(optimal_portfolio, axis=1).sum(axis=1).mean()
annual_return_test = (1 + mean_return_test)**252-1
print("Annual return of test data", annual_return_test)