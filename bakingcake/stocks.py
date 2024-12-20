"""
This module will house all stock related functions.
"""
import datetime
import pandas as pd
import yfinance as yf


def get_price_action(
        ticker_list,
        start=datetime.datetime.today() - datetime.timedelta(days=31),
        end=datetime.datetime.today() - datetime.timedelta(days=1)):
    """
        This method will pull the stock price volatility given a list of
        tickers and a start and end date.

        Args:
            ticker_list (list): list of tickers
            start (datetime.datetime): start date
            end (datetime.datetime): end date

        Returns:
            historical pricing DataFrame
    """
    cols = ["ticker", "open", "close", "low", "high"] #, "changePercent"]
    price_action_list = []
    # Iterate over each ticker and add information to the DataFrame
    for ticker in ticker_list:

        # Fetch the ticker data
        ticker_data = yf.Ticker(ticker)
        df = ticker_data.history(start=start, end=end)
        df.index.name = "date"

        df.rename(columns={
            i: i.lower() for i in price_action.columns
        })

        #df = get_historical_data(ticker, start, end)
        #df["ticker"] = ticker

        """
        # Set name of index to date
        #df.index = df.index.set_names(['date'])
        # Cast values to floating point numbers
        for column in cols[1:]:
            df[column] = df[column].astype(float)
        """

        # Append DataFrame to list
        price_action_list.append(df.loc[:, cols])
    

    return pd.concat(price_action_list).reset_index()
