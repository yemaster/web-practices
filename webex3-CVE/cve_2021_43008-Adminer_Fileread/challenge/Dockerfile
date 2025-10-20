FROM vulhub/adminer:4.6.2

# 拷贝容器入口点脚本
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

# 设置容器入口点
ENTRYPOINT [ "sh", "/docker-entrypoint.sh" ]