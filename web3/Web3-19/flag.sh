#!/bin/sh
sed -i "s/flag{.*}/${GZCTF_FLAG}/g" /var/www/html/flag.php
unset GZCTF_FLAG
nginx &
php-fpm