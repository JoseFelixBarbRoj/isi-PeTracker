FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install .

EXPOSE 8000