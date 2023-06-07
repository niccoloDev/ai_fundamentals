import random
from datetime import datetime

import pandas as pd
import yfinance as yf

from business_logic.model import Asset


class DataLoader:
    @staticmethod
    def load_assets(tickers, start_date, end_date):
        assets = []

        tickers = DataLoader._set_tickers(tickers)

        for ticker in tickers:
            data = yf.download(ticker, start=start_date, end=end_date)
            assets.append(Asset(ticker, data))

        # validate assets list removing assets with not enough values
        # longest_sequence = max([len(asset.data) for asset in assets])
        min_len = DataLoader._compute_min_data_len(start_date, end_date)
        for i in range(len(assets)):
            if len(assets[i].data) < min_len:
                assets[i] = DataLoader._replace_asset(min_len, start_date, end_date)

        return assets

    @staticmethod
    def _replace_asset(target_len, start_date, end_date):
        # fallback_tickers = ['TSLA','GC=F','ETH-USD','NFLX','EURUSD=X']
        data = None
        ticker = None
        max_iter = 100
        count = 0
        while True:
            count += 1
            ticker = DataLoader._fetch_nasdaq_tickers(1)[0]
            data = yf.download(ticker, start=start_date, end=end_date)
            if len(data) > target_len:
                break
            if count > max_iter:
                raise Exception('Random ticker fetch timeout reached')
                # ticker = random.choice(fallback_tickers)
                # data = yf.download(ticker, start=start_date, end=end_date)
        return Asset(ticker, data)

    @staticmethod
    def _fetch_nasdaq_tickers(count):
        url = 'http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt'
        df = pd.read_csv(url, sep='|')
        tickers = df['Symbol'].tolist()[:-1]
        return random.sample(tickers, count)

    @staticmethod
    def _set_tickers(tickers):
        if isinstance(tickers, int):  # if the user passed a number n we pick n random tickers
            return DataLoader._fetch_nasdaq_tickers(tickers)
        else:  # else the user passed a comma separated string with the tickers and we convert it to a list
            return tickers.split(',')

    # we accept the ticker's data if it has at least the data for the 60% of the trading days of the period specified
    @staticmethod
    def _compute_min_data_len(start_date, end_date):
        time_period = end_date - start_date
        trading_days_perc = 252 / 365
        actual_trading_days = time_period.days * trading_days_perc
        return actual_trading_days * 0.6







