FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir boto3 requests

CMD ["sh", "-c", "./script.sh"]
