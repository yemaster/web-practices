#!/bin/sh
echo "$GZCTF_FLAG" > /flag
GZCTF_FLAG=""
unset GZCTF_FLAG
gunicorn --bind 0.0.0.0:80 app:app