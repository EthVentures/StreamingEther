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

class BitTrex_Market(object):
    """BitTrex Market Data"""
    def __init__(self):
        self.api_url = settings.BITTREX_API_URL
        self.exchange = "bittrex"
        if settings.BITTREX_API_URL[-1] == "/":
            self.api_url = settings.BITTREX_API_URL[:-1]


    def clean(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["Ask"])
        clean_data["bid"] = float(data["Bid"])
        clean_data["price"] = float(data["Last"])
        return clean_data

    def get_ticker(self,product):
        """Get current tick"""
        payload = {'market': product}
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.post(self.api_url + '/v1.1/public/getticker', data=payload)
        data = loads(r.text)
        data = self.clean(data["result"])
        data["tracker_timestamp"] = now
        data["product"] = product
        data["exchange"] = self.exchange
        return data
