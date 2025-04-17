#!/bin/sh
echo $GZCTF_FLAG > /flag
unset GZCTF_FLAG
nginx &
php-fpm