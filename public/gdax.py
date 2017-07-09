#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:29:13 2017

@authors: avelkoski
         dconroy
"""
from json import loads
from datetime import datetime
import settings
import logging
import requests

logging.basicConfig(level=logging.INFO)

class GDAX_Market(object):
    """GDAX Market Data"""
    def __init__(self):
        self.api_url = settings.GDAX_API_URL
        self.exchange = "gdax"
        self.books = ['asks','bids']
        if settings.GDAX_API_URL[-1] == "/":
            self.api_url = settings.GDAX_API_URL[:-1]

    def clean_ticker(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["ask"])
        clean_data["bid"] = float(data["bid"])
        clean_data["price"] = float(data["price"])
        clean_data["volume"] = float(data["volume"])
        clean_data["size"] = float(data["size"])
        clean_data["timestamp"] = data["time"]
        return clean_data


    def clean_book(self,data,product,now):
        docs = {}
        for book in self.books:
            docs[book] = []
            for order in data[book]:
                source = {'type':book,'price':float(order[0]),'size':float(order[1]),'order_id':order[2],'exchange':self.exchange,'product':product,'tracker_timestamp':now}
                docs[book].append(source)
        return docs

    def get_ticker(self,product):
        """Get current tick"""
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.get(self.api_url + '/products/' + product + '/ticker')
        data = loads(r.text)
        data = self.clean_ticker(data)
        data["tracker_timestamp"] = now
        data["product"] = product
        data["exchange"] = self.exchange
        return data

    def get_book(self,product,level):
        """Get order book"""
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.get(self.api_url + '/products/' + product + '/book?level=' + level)
        data = loads(r.text)
        data = self.clean_book(data,product,now)
        return data
    

