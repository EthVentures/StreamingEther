#!/usr/bin/env python
from __future__ import print_function
from threading import Event
from satori.rtm.client import make_client, SubscriptionMode
from public.kraken import Kraken_Market
from public.gdax import GDAX_Market
from public.poloniex import Poloniex_Market
from public.bitfinex import BitFinex_Market
from public.bittrex import BitTrex_Market
from public.gemini import Gemini_Market
from dotenv import Dotenv
from time import sleep
import satori.rtm.auth as auth
import logging
import schedule
import settings
import sys

logging.basicConfig(level=logging.info)

channel = "complete-ethereum-market-data"
endpoint = "wss://open-data.api.satori.com"
role = "complete-ethereum-market-data"
appkey = settings.SATORI_APPKEY
secret = settings.SATORI_SECRET

gdax_market = GDAX_Market()
poloniex_market = Poloniex_Market()
gemini_market = Gemini_Market()
kraken_market = Kraken_Market()
bittrex_market = BitTrex_Market()
bitfinex_market = BitFinex_Market()


def main():

    print('Creating RTM client instance')

    if role and secret:
        auth_delegate = auth.RoleSecretAuthDelegate(role, secret)
    else:
        auth_delegate = None

    with make_client(
            endpoint=endpoint, appkey=appkey,
            auth_delegate=auth_delegate) as client:

        publish_finished_event = Event()

        def get_ticks():
            client.publish(channel, message=gdax_market.get_ticker(
                'ETH-USD'), callback=publish_callback)
            client.publish(channel, message=poloniex_market.get_ticker(
                'USDT_ETH'), callback=publish_callback)
            client.publish(channel, message=gemini_market.get_ticker(
                'ETHUSD'), callback=publish_callback)
            client.publish(channel, message=kraken_market.get_ticker(
                'XETHZUSD'), callback=publish_callback)

        def get_candles():
            client.publish(channel, message=poloniex_market.get_candle(
                'USDT_ETH', '300'), callback=publish_callback)

        def publish_callback(ack):
            if ack['action'] == 'rtm/publish/ok':
                print('Publish OK')
                publish_finished_event.set()
            elif ack['action'] == 'rtm/publish/error':
                print(
                    'Publish request failed, error {0}, reason {1}'.format(
                        ack['body']['error'], ack['body']['reason']))
                sys.exit(1)

        logging.info('Initializing Schedules for Ticks and Candles')

        schedule.every(settings.MARKET_REFRESH_RATE).seconds.do(get_ticks)
        schedule.every(settings.CANDLE_REFRESH_RATE).seconds.do(get_candles)

        # Get and Record market data
        while True:
            try:
                schedule.run_pending()
                sleep(1)
            except:
                sleep(1)
                continue

if __name__ == '__main__':
    main()
