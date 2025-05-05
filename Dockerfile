FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./sample_hello.py /app/sample_hello.py

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "8080"]