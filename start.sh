#!/bin/bash
#pproxy -l http://:8118 -r socks5://127.0.0.1:9050 -vv &
#PPROXY_PID=$!

#tor -f etc/tor/torrc &
#TOR_PID=$!

cd crawler/
scrapy crawl gasoline_spider
cd ../

python -m app.app --data-path crawler/output.parquet
