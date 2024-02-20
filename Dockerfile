FROM alpine:latest

RUN mkdir -p /app && \
    apk add --no-cache tini curl python3 py3-bottle py3-paste && \
    curl -s https://raw.githubusercontent.com/scaleway/scaleway-cli/master/scripts/get.sh | ash

COPY start.sh /app/start.sh
COPY serve.py /app/serve.py

WORKDIR /app

ENV USER="demo"
ENV PASS="test"

EXPOSE 8000

ENTRYPOINT ["/app/start.sh"]
