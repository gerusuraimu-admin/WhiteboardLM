FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./whiteboardlm /app/whiteboardlm
COPY ./main.py /app/main.py

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt \

ENV PORT 8080

CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "8080"]