#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:29:13 2017

@authors: avelkoski
         dconroy
"""
from json import loads
from datetime import datetime, timedelta
import settings
import logging
import requests

logging.basicConfig(level=logging.INFO)

class Poloniex_Market(object):
    """Poloniex Market Data"""
    def __init__(self):
        self.api_url = settings.POLONIEX_API_URL
        self.exchange = "poloniex"
        self.books = ['asks','bids']
        if settings.POLONIEX_API_URL[-1] == "/":
            self.api_url = settings.POLONIEX_API_URL[:-1]

    def clean_ticker(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["lowestAsk"])
        clean_data["bid"] = float(data["highestBid"])
        clean_data["price"] = float(data["last"])
        clean_data["volume"] = float(data["baseVolume"])
        return clean_data

    def clean_book(self,data,product,now):
        docs = {}
        for book in self.books:
            docs[book] = []
            for order in data[book]:
                source = {'type':book,'price':float(order[0]),'size':float(order[1]),'exchange':self.exchange,'product':product,'tracker_timestamp':now}
                docs[book].append(source)
        return docs

    def clean_candle(self,data,product):
        for i,tick in enumerate(data):
            del tick['weightedAverage']
            del tick['quoteVolume']
            tick['timestamp'] = datetime.strftime(datetime.utcfromtimestamp(tick['date']),'%Y-%m-%dT%H:%M:%S.%fZ')
            del tick['date']
            data[i] = tick
        return {'candles':data}

    def get_ticker(self,product):
        """Get current tick"""
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.get(self.api_url + '/public?command=returnTicker')
        data = loads(r.text)
        data = self.clean_ticker(data[product])
        data["tracker_timestamp"] = now
        data["product"] = product
        data["exchange"] = self.exchange
        return data

    def get_book(self,product,level):
        """Get order book"""
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.get(self.api_url + '/public?command=returnOrderBook&currencyPair=' + product + '&depth=' + level)
        data = loads(r.text)
        data = self.clean_book(data,product,now)
        return data

    def get_candle(self,product,period):
        """Get candles"""
        end, utc = datetime.now(), datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        start = (end - timedelta(1))
        r = requests.get(self.api_url + '/public?command=returnChartData&currencyPair=' + product + '&start=' + start.strftime("%s") + '&end=' + end.strftime("%s") + '&period=' + period)
        data = loads(r.text)
        data = self.clean_candle(data,product)
        data['timestamp'] = utc
        data["product"] = product
        data["period"] = period
        data["exchange"] = self.exchange
        return data

