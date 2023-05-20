import finnhub
import numpy as np
import math


class StocksAPI:
    def __init__(self):
        # Setup client
        self.finnhub_client = finnhub.Client(api_key="chib3b1r01qotr0m27b0chib3b1r01qotr0m27bg")

    def get_stock_data(self, stock_symbol, timestamp_start, timestamp_end):
        res = self.finnhub_client.stock_candles(stock_symbol, 'D', timestamp_start, timestamp_end)
        no_data_points = len(res['h'])
        stock_data = []
        for entry in range(no_data_points):
            stock_day = StocksDay(res['c'][entry], res['h'][entry], res['l'][entry], res['o'][entry], res['t'][entry])
            stock_data.append(stock_day)
        return stock_data

    def get_stock_cumulative_return(self, stock_symbol, timestamp_start, timestamp_end):
        first_day_res = self.finnhub_client.stock_candles(stock_symbol, 'D', timestamp_start, timestamp_start)
        last_day_res = self.finnhub_client.stock_candles(stock_symbol, 'D', timestamp_end, timestamp_end)
        first_day_value = first_day_res['h'][0]
        last_day_value = last_day_res['h'][0]
        cumulative_result = last_day_value / first_day_value - 1
        return cumulative_result

    def get_volatility(self, stock_symbol, timestamp_start, timestamp_end):
        res = self.finnhub_client.stock_candles(stock_symbol, 'D', timestamp_start, timestamp_end)
        no_data_points = len(res['h'])
        std_deviation = np.std(res['h'])
        return math.sqrt(no_data_points) * std_deviation


class StocksDay:
    def __init__(self, c, h, l, o, t):
        self.close = c
        self.high = h
        self.low = l
        self.open = o
        self.timestamp = t
