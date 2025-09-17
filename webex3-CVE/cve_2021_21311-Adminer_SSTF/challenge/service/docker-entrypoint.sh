#!/bin/sh
rm -f /docker-entrypoint.sh

# Get the user
user=$(ls /home)

# Check the environment variables for the flag and assign to INSERT_FLAG
# 需要注意，以下语句会将FLAG相关传递变量进行覆盖，如果需要，请注意修改相关操作
if [ "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
    export DASFLAG=no_FLAG
    DASFLAG=no_FLAG
elif [ "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
    export FLAG=no_FLAG
    FLAG=no_FLAG
elif [ "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
    export GZCTF_FLAG=no_FLAG
    GZCTF_FLAG=no_FLAG
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi

# 把 /app/app.py 的 flag{xxx} 替换为 INSERT_FLAG
sed -i "s/flag{.*}/$INSERT_FLAG/" /app/app.py

chmod 740 /app/*

php-fpm & nginx &

cd /app && flask run -h 127.0.0.1 -p 8888 &

echo "Running..."

tail -F /var/log/nginx/access.log /var/log/nginx/error.log