#!/bin/sh
echo "127.0.0.1 web" >> /etc/hosts
sed -i "s/flag{.*}/${GZCTF_FLAG}/g" /app/app.py
unset GZCTF_FLAG
hypercorn app:app --bind 127.0.0.1:80