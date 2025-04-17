#!/bin/sh
length=${#GZCTF_FLAG}
split_index=$((length / 2))
flag_1=${GZCTF_FLAG:0:split_index}
flag_2=${GZCTF_FLAG:split_index}
sed -i "s/flag{.*}/$flag_1/" /app/app.py
echo $flag_2 > /flag
unset GZCTF_FLAG
unset flag_1
unset flag_2
nginx &
su nobody -s /bin/sh -c 'gunicorn --bind 127.0.0.1:8000 app:app'