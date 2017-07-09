# settings.py
import os
from dotenv import Dotenv
dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
os.environ.update(dotenv)

MARKET_REFRESH_RATE = int(os.environ.get("MARKET_REFRESH_RATE"))
CANDLE_REFRESH_RATE = int(os.environ.get("CANDLE_REFRESH_RATE"))

GDAX_API_URL = os.environ.get("GDAX_API_URL")
KRAKEN_API_URL = os.environ.get("KRAKEN_API_URL")
BITFINEX_API_URL = os.environ.get("BITFINEX_API_URL")
BITTREX_API_URL = os.environ.get("BITTREX_API_URL")
GEMINI_API_URL = os.environ.get("GEMINI_API_URL")
POLONIEX_API_URL = os.environ.get("POLONIEX_API_URL")
POLONIEX_API_KEY = os.environ.get("POLONIEX_API_KEY")

SATORI_APPKEY = os.environ.get("SATORI_APPKEY")
SATORI_SECRET = os.environ.get("SATORI_SECRET")

ELASTICSEARCH_CONNECT_STRING = os.environ.get("ELASTICSEARCH_CONNECT_STRING")
