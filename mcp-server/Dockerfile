FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple

COPY server.py .
COPY data ./data

EXPOSE 8000

CMD ["python", "server.py"]
