#!/usr/bin/python3
import requests as req
import time

base_url = "http://192.168.1.1/cgi-bin/webui"
login_url = base_url + "/admin"

def get_token():
    token = {}
    resp = req.get(login_url)
    for line in resp.text.split('\n'):
        if 'timestamp' in line:
            token['timestamp'] = line.split('"')[1]
        if 'csrftoken' in line:
            token['csrftoken'] = line.split('"')[1]
            break
    return token


def get_cookie():
    token = get_token();
    payload='username=admin&password=Forgus%401876&csrftoken=' + token['csrftoken'] + '&timestamp=' + token['timestamp']
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
    resp = req.post(login_url,headers=headers,data=payload)
    resp_headers = resp.request.headers 
    return resp_headers['Cookie']

