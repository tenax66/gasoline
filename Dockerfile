FROM python:3.12-slim

WORKDIR /code

COPY ./app/ ./app/
COPY ./src/gasoline/ ./src/gasoline/
COPY pyproject.toml .
COPY requirements.txt .
COPY README.md .
COPY crawler/output.parquet .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install .

EXPOSE 8000

CMD ["python", "-m", "app.app", "--data-path", "output.parquet"]
