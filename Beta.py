import pandas_datareader as web
from datetime import datetime
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
#Collects closing prices and saves it on csv for later or offline use
def get_data(symbols,start,end):
    df_main = pd.DataFrame()
    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")
    for symbol in symbols:
        if not os.path.exists("stock_dfs/{}.csv".format(symbol)):
            df_temp = web.DataReader("{}".format(symbol),"morningstar")
            df_temp.to_csv("stock_dfs/{}.csv".format(symbol))
        else:
            print("{} exists".format(symbol))

        df_join = pd.read_csv("stock_dfs/{}.csv".format(symbol),index_col="Date",parse_dates=True, usecols= ["Date","Close"],na_values = ["nan"])
        df_join = df_join.rename(columns = {"Close": symbol})
        df_join=df_join.pct_change()
        df_main = df_main.join(df_join.loc[start:end],how="right")
    return df_main
def beta_alpha(data, single_stock, market="SPY"):
    data.plot(kind='scatter',x='SPY', y =single_stock)
    beta_stock, alpha_stock =np.polyfit(data["SPY"],data[single_stock],1)
    print("beta_{}=".format(single_stock),beta_stock)
    print("alpha_{}=".format(single_stock),alpha_stock)
    plt.plot(data["SPY"], beta_stock*data['SPY'] + alpha_stock,'-',color='r')
    plt.show()
symbols = ["SPY","TSLA"]
start = datetime(2015,1,1)
end = datetime(2016,1,10)
data = get_data(symbols,start,end)
beta_alpha(data,"TSLA")

