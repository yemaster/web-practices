#!/bin/sh
echo $GZCTF_FLAG > /flag
unset GZCTF_FLAG
nginx &
su nobody -s /bin/sh -c 'npm run start'