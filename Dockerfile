FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade pip

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
