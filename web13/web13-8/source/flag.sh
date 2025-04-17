#!/bin/sh
echo $GZCTF_FLAG > /flag
unset GZCTF_FLAG
nginx &
su nobody -s /bin/sh -c 'gunicorn --bind 127.0.0.1:8000 app:app'