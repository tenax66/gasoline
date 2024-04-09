FROM python:3.12-slim

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
