FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY /src .

COPY requirements.txt .

RUN apk add libffi-dev gcc libc-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache
