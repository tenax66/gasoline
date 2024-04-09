FROM python:3.12-slim

# tor
# Install necessary packages
RUN apt-get update && apt-get install -y tor privoxy

# Configure Tor
RUN echo "VirtualAddrNetwork 10.192.0.0/10" >> /etc/tor/torrc
RUN echo "AutomapHostsOnResolve 1" >> /etc/tor/torrc
RUN echo "TransPort 9040" >> /etc/tor/torrc
RUN echo "DNSPort 5353" >> /etc/tor/torrc

# Expose Tor's SOCKS proxy port
EXPOSE 9050

# Configure Privoxy
RUN echo "forward-socks5 / localhost:9050 ." >> /etc/privoxy/config

RUN service tor start && service privoxy start

# Expose Privoxy port
EXPOSE 8118

WORKDIR /code

COPY ./app/ ./app/
COPY ./src/gasoline/ ./src/gasoline/
COPY pyproject.toml .
COPY requirements.txt .
COPY README.md .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install .

# crawl
COPY ./crawler ./crawler
RUN cd crawler && scrapy crawl gasoline_spider

EXPOSE 8000

CMD ["python", "-m", "app.app", "--data-path", "crawler/output.parquet"]
