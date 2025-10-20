#!/usr/bin/env bash
set -euo pipefail

# —— 读取 .env（由 docker-compose 注入）——
CACTI_VERSION="${CACTI_VERSION:-1.2.18}"
DB_ROOT_PASSWORD="${DB_ROOT_PASSWORD:-root_pass}"
DB_NAME="${DB_NAME:-cacti}"
DB_USER="${DB_USER:-cactiuser}"
DB_PASS="${DB_PASS:-cacti_pass}"

# FLAG1="${FLAG1:-default_user_flag}"
# FLAG2="${FLAG2:-default_root_flag}"

# # FLAG1 -> /userflag（所有用户可读）
# echo -n "${FLAG1}" > /userflag
# chmod 0644 /userflag
# unset FLAG1

# # FLAG2 -> /rootflag（仅 root 可读）
# echo -n "${FLAG2}" > /rootflag
# chmod 0600 /rootflag
# unset FLAG2


# —— 目录与权限（幂等）——
mkdir -p /var/lib/mysql /var/run/mysqld /var/www/cacti /var/lib/cacti/rra /var/log/cacti /etc/cron.d
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld || true
chmod -R 750 /var/lib/mysql /var/run/mysqld || true
chown -R cacti:cacti /var/www/cacti /var/lib/cacti /var/log/cacti || true

# —— 等待/启动 mysqld —— 
wait_for_mysqld() {
  local tries=0
  until mysqladmin ping >/dev/null 2>&1; do
    sleep 1
    tries=$((tries+1))
    if [ "$tries" -gt 60 ]; then
  # MariaDB 未能在 60 秒内响应
      return 1
    fi
  done
  return 0
}

# 初始化数据目录（如果为空）
if [ -z "$(ls -A /var/lib/mysql 2>/dev/null)" ]; then
  # 初始化 MariaDB 数据目录
  mysqld --initialize-insecure --user=mysql --datadir=/var/lib/mysql
fi

# 若还未运行，临时以 mysql 用户启动 mysqld_safe
if ! mysqladmin ping >/dev/null 2>&1; then
  # 临时启动 mysqld_safe
  su -s /bin/bash mysql -c "/usr/bin/mysqld_safe --datadir=/var/lib/mysql > /var/log/mysqld_safe.log 2>&1 &"
  wait_for_mysqld || { exit 1; }
fi

# —— 数据库：设置 root 密码、创建库与用户（幂等）——
## 创建/确认数据库与用户
mysql -u root <<SQL || true
ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASSWORD}';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\` CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
SQL

# —— 如未导入 schema，则自动寻找并导入（兼容多版本路径）——
if ! mysql -h127.0.0.1 -u"${DB_USER}" -p"${DB_PASS}" -e "USE ${DB_NAME}; SHOW TABLES;" | grep -q "poller"; then
  # 尝试自动导入 Cacti schema
  FOUND_SQL=""
  for CAND in \
      /var/www/cacti/cacti.sql \
      /var/www/cacti/include/sql/cacti.sql \
      /var/www/cacti/database/cacti.sql \
      /var/www/cacti/sql/cacti.sql \
      /var/www/cacti/include/sql/*.sql
  do
    for f in $CAND; do
      [ -f "$f" ] && FOUND_SQL="$f" && break 2
    done
  done
  if [ -n "$FOUND_SQL" ]; then
    mysql -h127.0.0.1 -u"${DB_USER}" -p"${DB_PASS}" "${DB_NAME}" < "$FOUND_SQL"
    mysql -h127.0.0.1 -u"${DB_USER}" -p"${DB_PASS}" "${DB_NAME}" -e "UPDATE user_auth SET must_change_password='' WHERE username = 'admin'"
  fi
fi

# —— 确保 MySQL 时区表已填充，并授予 Cacti 查询权限 ——
## 检查 MySQL 时区表
TZ_COUNT=$(mysql -h127.0.0.1 -uroot -p"${DB_ROOT_PASSWORD}" -Nse \
  "SELECT COUNT(*) FROM mysql.time_zone_name;" 2>/dev/null || echo 0)

if [ "${TZ_COUNT}" = "0" ]; then
  # 填充 MySQL 时区表（mysql.time_zone*）
  mysql_tzinfo_to_sql /usr/share/zoneinfo | \
    mysql -h127.0.0.1 -uroot -p"${DB_ROOT_PASSWORD}" mysql || true
fi

## 授予 Cacti 账户读取时区表权限
mysql -h127.0.0.1 -uroot -p"${DB_ROOT_PASSWORD}" -e \
  "GRANT SELECT ON mysql.time_zone_name TO '${DB_USER}'@'localhost'; \
   GRANT SELECT ON mysql.time_zone TO '${DB_USER}'@'localhost'; \
   GRANT SELECT ON mysql.time_zone_transition TO '${DB_USER}'@'localhost'; \
   GRANT SELECT ON mysql.time_zone_transition_type TO '${DB_USER}'@'localhost'; \
   GRANT SELECT ON mysql.time_zone_leap_second TO '${DB_USER}'@'localhost'; \
   FLUSH PRIVILEGES;" || true

# 可选：将全局时区设为 UTC（运行时）
mysql -h127.0.0.1 -uroot -p"${DB_ROOT_PASSWORD}" -e "SET GLOBAL time_zone='UTC';" || true
# —— 强制重写 Cacti 配置（满足你的 3 条要求）——
# 1. 始终覆盖为 .env 中的 DB 凭据
# 2. 强制使用 TCP：host=127.0.0.1, port=3306
# 3. 路由使用根路径：$url_path = ''
CFG="/var/www/cacti/include/config.php"
mkdir -p /var/www/cacti/include
cat > "${CFG}" <<PHP
<?php
\$database_type     = 'mysql';
\$database_default  = '${DB_NAME}';
\$database_hostname = '127.0.0.1';
\$database_username = '${DB_USER}';
\$database_password = '${DB_PASS}';
\$database_port     = '3306';
\$database_retries  = 5;
\$database_ssl      = false;
\$database_persist  = false;

\$poller_id = 1;

/* 根路径路由（不使用 /cacti/） */
\$url_path = '';

/* 其他保留默认 */
\$cacti_session_name = 'Cacti';
\$disable_log_rotation = false;
PHP
chown cacti:cacti "${CFG}" || true
chmod 0640 "${CFG}" || true
## 已强制写入 config.php

# —— cron：每分钟跑 poller —— 
CRONFILE="/etc/cron.d/cacti_poller"
cat > "${CRONFILE}" <<CRON
*/1 * * * * cacti php /var/www/cacti/poller.php > /var/log/cacti/poller.log 2>&1
CRON
chmod 0644 "${CRONFILE}" || true

# 收尾权限
chown -R cacti:cacti /var/www/cacti || true
chown -R mysql:mysql /var/lib/mysql || true

## dock_init.sh 完成
exit 0