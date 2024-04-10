#!/bin/bash
# pproxy

echo "Starting pproxy..."
pproxy -l http+socks4://:8118 -r socks5://127.0.0.1:9050 &
while ! nc -z localhost 8118; do
  sleep 1
done
echo "pproxy started successfully."

# tor
echo "Starting Tor..."
tor &
while ! nc -z localhost 9050; do
  sleep 1
done
echo "Tor started successfully."

sleep 60

# Start scrapy
echo "Starting Scrapy..."

cd crawler/
scrapy crawl gasoline_spider
cd ../

python -m app.app --data-path crawler/output.parquet
