#!/bin/sh
echo "127.0.0.1 web" >> /etc/hosts
service dbus start

sed -i "s/flag{.*}/${GZCTF_FLAG}/g" /app/app.py
unset GZCTF_FLAG
nginx &
# 使用 user 用户运行
hypercorn app:app --bind 127.0.0.1:5000