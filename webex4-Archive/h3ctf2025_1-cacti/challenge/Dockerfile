# 基础镜像
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# —— 换源到 USTC —— 
RUN set -eux; \
    sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list.d/ubuntu.sources;\
    sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/ubuntu.sources

# 安装运行时依赖
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates wget curl gnupg lsb-release \
    apache2 php php-cli php-mysql php-snmp php-gd php-xml php-mbstring php-pear php-intl\
    php-gmp php-ldap \
    mariadb-server mariadb-client \
    snmp snmpd rrdtool \
    cron unzip supervisor git python3 \
 && rm -rf /var/lib/apt/lists/*

# 创建低权限用户
RUN useradd -m -s /bin/bash cacti || true \
 && mkdir -p /var/www/cacti /var/lib/cacti/rra /var/log/cacti \
 && chown -R cacti:cacti /var/www/cacti /var/lib/cacti /var/log/cacti

# 准备 mysql 目录权限
RUN mkdir -p /var/lib/mysql /var/run/mysqld \
 && chown -R mysql:mysql /var/lib/mysql /var/run/mysqld \
 && chmod -R 750 /var/lib/mysql /var/run/mysqld

# 修改 Apache 运行用户
RUN sed -i 's/APACHE_RUN_USER=www-data/APACHE_RUN_USER=cacti/' /etc/apache2/envvars \
 && sed -i 's/APACHE_RUN_GROUP=www-data/APACHE_RUN_GROUP=cacti/' /etc/apache2/envvars \
 && a2enmod rewrite

# 复制本地的 Cacti 源码包
COPY cacti-1.2.28.tar.gz /tmp/cacti-1.2.28.tar.gz
RUN tar -xzf /tmp/cacti-1.2.28.tar.gz -C /var/www/cacti --strip-components=1 \
 && chown -R cacti:cacti /var/www/cacti \
 && rm -f /tmp/cacti-1.2.28.tar.gz

# 将已安装的 sudo 运行时打包件放进来
COPY sudo-runtime.tar.gz /tmp/sudo-runtime.tar.gz

# 解包到根目录，并设置 SUID、刷新动态链接缓存
RUN tar -C / -xzf /tmp/sudo-runtime.tar.gz \
 && rm -f /tmp/sudo-runtime.tar.gz \
 && mkdir -p /usr/local/bin \
 && if [ -f /usr/bin/sudo ]; then mv /usr/bin/sudo /usr/local/bin/; fi \
 && if [ -f /usr/local/bin/sudo ]; then chown root:root /usr/local/bin/sudo && chmod 4755 /usr/local/bin/sudo; fi \
 # 确保 /usr/lib 在动态库搜索路径中，并刷新缓存
 && echo "/usr/lib" > /etc/ld.so.conf.d/usr-local-lib.conf \
 && ldconfig

RUN mkdir -p /usr/etc \
 && printf "root ALL=(ALL) ALL\n" > /etc/sudoers \
 && chown root:root /etc/sudoers \
 && chmod 440 /etc/sudoers

# 拷贝配置文件
COPY cacti_apache.conf /etc/apache2/sites-available/000-cacti.conf
RUN a2ensite 000-cacti || true

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY dock_init.sh /usr/local/bin/dock_init.sh
RUN chmod +x /usr/local/bin/dock_init.sh

EXPOSE 80
# CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

COPY clean.sh /root/clean.sh
RUN chmod +x /root/clean.sh

ENTRYPOINT [ "/bin/bash", "/root/clean.sh" ]