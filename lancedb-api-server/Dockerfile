FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    lancedb \
    pandas \
    pyarrow \
    numpy \
    pydantic

COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
