import requests as req
import base64
import json


def base64_encode(param):
    return str(base64.b64encode(param.encode('utf-8')))


def login(base_url, password):
    payload = json.dumps({
        "username": "admin",
        "pass": base64_encode(password),
        "passwd": "d77160f4d93ad05a88f50bed60e2dafd",
        "remember_password": "true"
    })
    headers = {
        'Content-Type': 'application/json',
    }
    resp = req.post(base_url + '/login',
                    headers=headers, data=payload)
    resp_headers = resp.headers
    return {'Cookie': resp_headers['Set-Cookie']}
