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

class Gemini_Market(object):
    """Gemini Market Data"""
    def __init__(self):
        self.api_url = settings.GEMINI_API_URL
        self.exchange = "gemini"
        self.books = ['asks','bids']
        if settings.GEMINI_API_URL[-1] == "/":
            self.api_url = settings.GEMINI_API_URL[:-1]

    def clean_ticker(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["ask"])
        clean_data["bid"] = float(data["bid"])
        clean_data["price"] = float(data["last"])
        clean_data['volume'] = float(data['volume']['ETH'])
        return clean_data

    def clean_book(self,data,time,product):
        docs = []
        for book in self.books:
            for order in data[book]:
                source = {'type':book,'price':float(order[0]),'size':float(order[1]),'order_id':order[2],'exchange':self.exchange,'book_time':time,'product':product}
                doc ={'_op_type':'index','_type':'book','_index':'eth.gemini.book','_source':source}
                docs.append(doc)
        return docs

    def get_ticker(self,product):
        """Get current tick"""
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.get(self.api_url + '/pubticker/' + product)
        data = loads(r.text)
        data = self.clean_ticker(data)
        data["tracker_timestamp"] = now
        data["product"] = product
        data["exchange"] = self.exchange
        return data

    def get_book(self,product):
        """Get order book"""
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.get(self.api_url + '/book/' + product) #default 50 https://docs.gemini.com/rest-api/#current-order-book
        data = loads(r.text)
        data = self.clean_book(data,now,product)
        return data
