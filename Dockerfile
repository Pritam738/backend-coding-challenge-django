FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV PATH="/home/user/.local/bin:${PATH}"

# Install sqlite3 on Alpine
RUN apk add --no-cache sqlite

WORKDIR /app

RUN adduser -D user && chown -R user:user /app
USER user

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./app /app
