# Streaming Ether
To promote others in creating open data channels on Satori, we have published the code that is supporting our [Streaming Ether Data Channel](https://www.satori.com/channels/complete-ethereum-market-data).

Streaming Ether (SE) provides a comprehensive view of the Ethereum market, without the hassle of writing custom libraries to interact with exchanges. Use this open dataset, which contains Timestamp (exchange / tracker), Price, Bid/Ask, Size, Depth of Market, Volume, and Candles, to test hypotheses about Ethereum, build machine learning models to predict price movements, understand volatility, arbitrage and more. SE enables high-quality cryptocurrency R&D across all major, global exchanges.


If you would like to configure Supervisor to manage automatic starts as well as restarts, we have also provided the configuration below.

```js
[program:satori_script]
command = /usr/bin/python /home/user/run.py
stdout_logfile = /var/log/watcher-stdout.log
stdout_logfile_maxbytes = 10MB
stdout_logfile_backups = 5
stderr_logfile = /var/log/watcher-stderr.log
stderr_logfile_maxbytes = 10MB
stderr_logfile_backups = 5
autostart=true
autorestart=true
```
