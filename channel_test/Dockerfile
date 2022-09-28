FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir psycopg2==2.9.3

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .
