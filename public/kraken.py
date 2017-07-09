#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:29:13 2017

@author: dconroy
"""
import requests
from json import loads
from datetime import datetime
import settings
import logging
import random

logging.basicConfig(level=logging.INFO)

class Kraken_Market(object):
    """ETH Kraken Market Data"""
    def __init__(self):
        self.api_url = settings.KRAKEN_API_URL
        self.exchange = "kraken"
        if settings.KRAKEN_API_URL[-1] == "/":
            self.api_url = settings.KRAKEN_API_URL[:-1]

    def clean(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["a"][0])
        clean_data["bid"] = float(data["b"][0])
        clean_data["price"] = float(data["c"][0])
        clean_data["volume"] = float(data["v"][1])
        return clean_data

    def get_ticker(self,product):
        """Get current tick"""
        payload = {'pair': product}
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.post(self.api_url + '/0/public/Ticker', data=payload)
        data = loads(r.text)
        data = self.clean(data["result"][product])
        data["tracker_timestamp"] = now
        data["product"] = product
        data["exchange"] = self.exchange
        return data