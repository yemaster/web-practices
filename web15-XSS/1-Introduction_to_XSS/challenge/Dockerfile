FROM debian:bookworm-slim

ARG PROJECT_PATH

RUN mkdir -p /app/chrome

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources
RUN apt update && apt install -y --no-install-recommends python3 python3-pip python3-selenium python3-quart python3-hypercorn nginx chromium-driver

RUN mkdir -p /run/nginx
COPY ${PROJECT_PATH}nginx.conf /etc/nginx/nginx.conf

WORKDIR /app
# COPY ${PROJECT_PATH}requirements.txt .
# RUN pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/simple
COPY ${PROJECT_PATH}app/ .

COPY ${PROJECT_PATH}flag.sh /etc/init.sh
RUN chmod +x /etc/init.sh
CMD ["sh", "/etc/init.sh"]