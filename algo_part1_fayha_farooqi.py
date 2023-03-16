#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt

class IndicatorsTA():
    def __init__(self, ticker: str, start_date: str, end_date: str):
        #Using yfinance, this will download daily stock data for a given ticker within a specific time range into a df.
        self.stockdf = yf.download(ticker, start=start_date, end=end_date, progress=False)
        self.algodf = self.getIndicators()
        
    def self__getRSI(self, window : int = 14) -> pd.DataFrame:
        #Calculate RSI
        rsi = ta.rsi(self.stockdf['Close'], window=window)
        
        #This will provide output df with column name.
        rsi_name = "RSI(" + str(window) + ")"
        data_rsi = {rsi_name: rsi}
        return pd.DataFrame(data_rsi)
    
    def self__getBBands(self, period : int = 20, stdev : int = 2) -> pd.DataFrame:
        # Calculate BBands
        upper_band, middle_band, lower_band = ta.bollinger_bands(self.stockdf['Close'], window=period, std=stdev)

        # Return a new dataframe with columns named a specified time range and stdev values
        bbands_df = pd.DataFrame({'LBand({},{})'.format(period, stdev): lower_band,
                                  'MBand({},{})'.format(period, stdev): middle_band,
                                  'HBand({},{})'.format(period, stdev): upper_band
                                 })

        return bbands_df
    
    def self__getVWAP(self) -> pd.DataFrame:
        #This calculates the cumulative volume and cumulative volume * stock price. 
        cum_volume = self.stockdf['Volume'].cumsum()
        cum_volume_price = (self.stockdf['Volume'] * self.stockdf['Adj Close']).cumsum()
        
        #This is the VWAP formula.
        vwap = cum_volume_price / cum_volume
        
        #This will provide output df with column name.
        vwap_name = "VWAP"
        data_vwap = {vwap_name: vwap}
        return pd.DataFrame(data_vwap)

    
    def self__getIndicators(self): 
        #Convert the functions to variables.
        rsi_df = __getRSI(window=window)
        bbands_df = __getBBands(period=period, stdev=stdev)
        vwap_df = __getVWAP()
    
        #Df with Adj Close and the 3 indicators.
        total_df = pd.concat([self.stockdf['Adj Close'], rsi_df, bbands_df, vwap_df], axis=1)
        return total_df
        
    def plotIndicators(self) -> None:
        #Using a single plot() call for each subplot and matplotlib.py to create a plot for the indicators.
        fig, axs = plt.subplots(3, 1, figsize=(15, 10), sharex=True)
    
        axs[0].plot(self.algodf['Close'], label='Close')
        axs[0].legend(loc='upper left')
    
        axs[1].plot(self.algodf['RSI'], label='RSI')
        axs[1].axhline(y=30, linestyle='--', color='gray')
        axs[1].axhline(y=70, linestyle='--', color='gray')
        axs[1].legend(loc='upper left')
        
        axs[2].plot(self.algodf[['Close', 'MBand(20,2)', 'HBand(20,2)', 'LBand(20,2)']], label=['Close', 'MBand(20,2)', 'HBand(20,2)', 'LBand(20,2)'])
        axs[2].legend(loc='upper left')
        
        #Add labels to the plot.
        plt.xlabel('Date')
        plt.show()
        
        


# In[ ]:




