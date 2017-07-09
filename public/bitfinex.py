#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:29:13 2017

@author: dconroy
"""
from json import loads
from datetime import datetime
import settings
import logging
import requests
import random


class BitFinex_Market(object):
    """Bitfinex Market Data"""
    def __init__(self):
        self.api_url = settings.BITFINEX_API_URL
        self.exchange = 'bitfinex'
        if settings.BITFINEX_API_URL[-1] == "/":
            self.api_url = settings.BITFINEX_API_URL[:-1]

    def clean(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["ask"])
        clean_data["bid"] = float(data["bid"])
        clean_data["price"] = float(data["last_price"])
        clean_data["volume"] = float(data["volume"])
        clean_data["timestamp"] = datetime.strftime(datetime.utcfromtimestamp(float(data['timestamp'])),'%Y-%m-%dT%H:%M:%S.%fZ')
        return clean_data

    def get_ticker(self,product):
        """Get current tick"""
        now = datetime.strftime(datetime.utcnow(),'%Y-%m-%dT%H:%M:%S.%fZ')
        r = requests.get(self.api_url + '/v1/pubticker/' + product)
        data = loads(r.text)
        data = self.clean(data)
        data["exchange"] = self.exchange
        data["tracker_timestamp"] = now
        data["product"] = product
        return data
