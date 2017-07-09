# Eth Monitor
Monitoring CryptoCurrency exchanges to collect data for Satori. To run, rename default.env to  just .env , and fill in your satori app key and secret.


If you would like to configure Supervisor to manage automatic starts as well as restarts, you can use the configuration below.
Supervisor Conf

```js
[program:satori_script]
command = /usr/bin/python /root/EthSatori/run.py
stdout_logfile = /var/log/watcher-stdout.log
stdout_logfile_maxbytes = 10MB
stdout_logfile_backups = 5
stderr_logfile = /var/log/watcher-stderr.log
stderr_logfile_maxbytes = 10MB
stderr_logfile_backups = 5
autostart=true
autorestart=true
```
