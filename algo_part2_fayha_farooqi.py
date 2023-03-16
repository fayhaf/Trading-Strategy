#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import yfinance as yf
import pandas_ta as ta

class backtest(IndicatorsTA):
    def __init__(self, ticker: str, start_date: str, end_date: str, quantity: float, position: bool):
        super().__init__(ticker, start_date, end_date)
        self.quantity = quantity
        self.position = position
        
         # Initialize cumulative percent returns dataframe
        self.cumulative_df = pd.DataFrame(index=self.stockdf.index)
        self.cumulative_df['Buy and Hold'] = self.stockdf['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)
        self.cumulative_df['RSI-BBands-VWAP'] = 0.0
        
        # Calculate indicators
        self.rsi_df = self.__getRSI()
        self.bbands_df = self.__getBBands()
        self.vwap_df = self.__getVWAP()
        
        # Generate signals
        self.signals = pd.DataFrame(index=self.stockdf.index)
        self.signals['Signal'] = 0
        self.signals.loc[self.rsi_df['RSI(14)'] < 30, 'Signal'] = 1  # Buy signal when RSI is below 30
        self.signals.loc[self.bbands_df['BBands_Lower'] > self.stockdf['Close'], 'Signal'] = 1  # Buy signal when price is below lower Bollinger Band
        self.signals.loc[self.vwap_df['VWAP'] < self.stockdf['Close'], 'Signal'] = -1  # Sell signal when price is above VWAP
        self.signals['Position'] = self.signals['Signal'].diff().fillna(0)
        
        # Calculate profits
        self.profits = pd.DataFrame(index=self.stockdf.index)
        self.profits['Profit'] = self.stockdf['Close'].pct_change() * self.signals['Position'] * self.quantity
        self.profits['Cumulative Returns'] = (self.profits['Profit'] + 1).cumprod().sub(1)
        self.cumulative_df['RSI-BBands-VWAP'] = self.profits['Cumulative Returns']
        
        # Close position at the end of the backtest
        if self.position:
            self.signals.loc[self.signals.index[-1], 'Position'] = -1
            
        def calculateReturns(self) -> pd.DataFrame:
        # Get indicators
        rsi = self.__getRSI(window=14)
        bbands = self.__getBollingerBands(window=20, num_std=2)
        vwap = self.__getVWAP()
        
        # Create signals based on indicators
        long_signals = ((self.stockdf['Close'] < bbands.iloc[:, 1]) & (rsi.iloc[:, 0] < 30) & (self.stockdf['Close'] < vwap.iloc[:, 0]))
        short_signals = ((self.stockdf['Close'] > bbands.iloc[:, 0]) & (rsi.iloc[:, 0] > 70) & (self.stockdf['Close'] > vwap.iloc[:, 0]))
        
        # Calculate returns
        buy_and_hold_returns = (self.stockdf['Close'].iloc[-1] - self.stockdf['Close'].iloc[0]) / self.stockdf['Close'].iloc[0]
        strategy_returns = []
        position = 0
        for i in range(len(self.stockdf)):
            if long_signals.iloc[i] and not self.position:
                position = self.quantity
                self.position = True
            elif short_signals.iloc[i] and self.position:
                position = -self.quantity
                self.position = False
            strategy_returns.append(position * (self.stockdf['Close'].iloc[i] - self.stockdf['Close'].iloc[i-1]) / self.stockdf['Close'].iloc[i-1])
        strategy_returns = pd.Series(strategy_returns).cumsum()[-1]
        
        # Create cumulative returns dataframe
        self.cumulative_df = pd.DataFrame({'Buy and Hold': (1 + buy_and_hold_returns) ** (252 / len(self.stockdf)) - 1,
                                           'Strategy': strategy_returns})
        
        return self.cumulative_df
    
        def PlotReturns(self):
            #Plot cumulative percent returns for both "Buy and Hold" and "Custom" strategies stored in the self.cumulative_df. 
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(self.cumulative_df.index, self.cumulative_df['Buy and Hold'], label='Buy and Hold')
            ax.plot(self.cumulative_df.index, self.cumulative_df['Custom'], label='Custom')
            ax.set_xlabel('Date')
            ax.set_ylabel('Cumulative Returns (%)')
            ax.set_title('Comparison of Buy and Hold vs. Custom Strategy')
            ax.legend()
            plt.show()

