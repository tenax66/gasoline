FROM python:3.12-slim

# Gasoline
WORKDIR /code

COPY ./app/ ./app/
COPY ./src/gasoline/ ./src/gasoline/
COPY pyproject.toml .
COPY requirements.txt .
COPY README.md .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install .

# tor
RUN apt-get update && apt-get install -y tor netcat-openbsd curl
COPY torrc ./etc/tor/torrc

EXPOSE 8000 8118 9050

# crawl
COPY ./crawler ./crawler
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]

