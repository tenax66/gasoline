# GASOLINE

https://www.technologyreview.jp/s/325142/recapturing-early-internet-whimsy-with-html/

[Small Website Discoverability Crisis](https://www.marginalia.nu/log/19-website-discoverability-crisis/)

# Get Started

```bash
#install
pip install --no-cache-dir --upgrade -r requirements.txt
pip install .

# create .parquet file
scrapy crawl gasoline_spider

# run
python -m app.app --data-path crawler/output.parquet
```

## Docker

```bash
docker build --tag gasoline:latest .
docker compose up
```

# Proxy Settings

```bash
pproxy -l http://:8118 -r socks5://127.0.0.1:9050 -vv
```

# Copyright

This software is based on [microsearch](https://github.com/alexmolas/microsearch).

Copyright (c) 2024 Alex Molas
