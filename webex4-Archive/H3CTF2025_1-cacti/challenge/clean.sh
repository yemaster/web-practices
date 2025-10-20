
echo `whoami`

FLAG=$GZCTF_FLAG

# 把 flag 按长度均匀分成三份
POS1=$(( ${#FLAG} / 3 ))
POS2=$(( POS1 * 2 ))
FLAG1=${FLAG:0:POS1}
export FLAG2=${FLAG:POS1:POS1}
FLAG3=${FLAG:POS2}

if [ $FLAG1 ]; then
  echo "flag-part1: $FLAG1" > /userflag
else
  echo "FLAG1{usrflagusrfsuursufrsufrsuf}" > /userflag
fi

if [ $FLAG2 ]; then
  echo "flag-part2: $FLAG2" > /rootflag
else
  echo "FLAG2{rootflagrootflagrootflagrootflag}" > /rootflag
fi

if [ $FLAG3 ]; then
  echo "flag-part3: $FLAG3" > /flag3
else
    echo "FLAG3{this_is_flag3_flag3_flag3_flag3}" > /flag3
fi

GZCTF_FLAG=''
unset GZCTF_FLAG
unset FLAG1
# unset FLAG2
unset FLAG3

# export FLAG1=''
# export FLAG3=''

chmod 0644 /userflag
chmod 0600 /rootflag
chmod 0600 /flag3

exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf

sleep infinity