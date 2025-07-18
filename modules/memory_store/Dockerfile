FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y procps && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

VOLUME /data
CMD ["python", "main.py"]
