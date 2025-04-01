FROM php:5.6-fpm-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk update && apk --no-cache add nginx
RUN mkdir -p /run/nginx
COPY nginx.conf /etc/nginx/nginx.conf
RUN sed -i "s#\/home\/www-data#\/players#g" /etc/passwd
RUN mkdir -p /players
RUN chown -R www-data:www-data /players
RUN chmod 755 /players
COPY src/ /var/www/html/
COPY flag.sh /etc/init.sh
RUN chmod +x /etc/init.sh
EXPOSE 80
CMD ["sh", "/etc/init.sh"]