FROM alpine:3.13-alpine

RUN mkdir -p /app/chrome

WORKDIR /app
COPY app/ .
COPY ../chrome/ ./chrome/

ENV CHROME_DRIVER_PATH=/app/chrome/chromedriver
ENV CHROME_EXECUTABLE_PATH=/app/chrome/chrome

COPY flag.sh /etc/init.sh
RUN chmod +x /etc/init.sh
CMD ["sh", "/etc/init.sh"]