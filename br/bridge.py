from binance.client import Client
from br.myapi import *
import pickle
import re
import os

def some_test():
    from_cache=True

    if from_cache==False:
        client = Client(api_key, api_secret)

        # get all symbol prices
        prices = client.get_all_tickers()

        # get market depth
        depth = client.get_order_book(symbol='BNBBTC')

        klines={}

        # fetch 1 minute klines for the last day up until now
        klines["1 day ago UTC, minute"] = client.get_historical_klines(
            "BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

        # fetch 30 minute klines for the last month of 2017
        klines["1 Dec, 2017 to 1 Jan, 2018, 30 minute"] = client.get_historical_klines(
            "ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

        # fetch weekly klines since it listed
        klines["1 Jan, 2017 to now, week"] = client.get_historical_klines(
            "NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

        # pickle them
        with open("klines.pkl","wb") as kline_pickle:
            pickle.dump(klines,kline_pickle)
            print('saved')

    else:
        with open("klines.pkl","rb") as kline_pickle:
            klines = pickle.load(kline_pickle)

            print('done')


class Bridge():
    def __init__(self):
        self.client = Client(api_key, api_secret)

    def get_prices(self):
        # get all symbol prices
        return self.client.get_all_tickers()

    def get_all_symbols(self):
        '''

        :param save:
        :return: a list of symbols string
        '''
        prices=self.get_prices()
        all_symbols=[i['symbol'] for i in prices]
        return all_symbols

    def get_klines(self, symbol, interval, start_str, end_str=None):

        '''
        :param symbol:
        :param interval:
        :param start_str:
        :param end_str:
        :return:

        Kline return value:

        1499040000000,  # Open time
        "0.01634790",  # Open
        "0.80000000",  # High
        "0.01575800",  # Low
        "0.01577100",  # Close
        "148976.11427815",  # Volume
        1499644799999,  # Close time
        "2434.19055334",  # Quote asset volume
        308,  # Number of trades
        "1756.87402397",  # Taker buy base asset volume
        "28.46694368",  # Taker buy quote asset volume
        "17928899.62484339"  # Can be ignored

        Open, high, low and close are price values.
        Volume and number of trades are trade signatures.
        '''

        print ("Getting "+symbol+" kline")
        return self.client.get_historical_klines(symbol, interval, start_str, end_str)

    def get_file_name(self,btc_symbol,interval=" 15 minute"):
        return "../data/btc_klines " + btc_symbol + interval+ ".pkl"

    def get_btc_symbols(self):
        symbols = self.get_all_symbols()
        pattern = re.compile("^([A-Za-z])*BTC$")
        btc_symbols = [i for i in symbols if pattern.match(i)]
        return btc_symbols

    def download_btc_klines(self, interval=Client.KLINE_INTERVAL_15MINUTE, start_str="1 May, 2017", end_str=None):
        btc_symbols=self.get_btc_symbols()

        btc_klines = {}
        for btc_symbol in btc_symbols:
            filename=self.get_file_name(btc_symbol)

            if os.path.isfile(filename):
                with open(filename,'rb') as kline_pickle:
                    print(filename+" exists")
            else:
                btc_klines[btc_symbol] = self.get_klines(btc_symbol, interval, start_str, end_str)
                with open(filename, "wb") as kline_pickle:
                    pickle.dump(btc_klines, kline_pickle)


if __name__=="__main__":
    bridge=Bridge()
    bridge.download_btc_klines()
