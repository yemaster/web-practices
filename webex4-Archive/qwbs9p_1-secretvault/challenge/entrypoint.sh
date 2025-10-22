#!/bin/sh

chmod 600 /entrypoint.sh

if [ ${GZCTF_FLAG} ];then
    echo -n ${GZCTF_FLAG} > /flag
    chown vault:nogroup /flag
    chmod 400 /flag
    echo [+] GZCTF_FLAG OK
    unset GZCTF_FLAG
else
    echo [!] no GZCTF_FLAG
fi

start_authorizer() {
    su authorizer -s /bin/sh -c /app/authorizer/authorizer &
}

start_vault() {
    cd /app/vault && FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())") su vault -s /bin/sh -c "python3 app.py" &
}

start_authorizer
start_vault

wait -n