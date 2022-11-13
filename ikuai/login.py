from urllib.parse import urlencode
import requests as req


class LoginPage():

    def __init__(self, base_url):
        self.login_page = req.get(base_url + '/login').text
        self.login_token = {}
        for line in self.login_page.split('\n'):
            if 'timestamp' in line:
                self.login_token['timestamp'] = line.split('"')[1]
            if 'csrftoken' in line:
                self.login_token['csrftoken'] = line.split('"')[1]
                break


def login(base_url, login_token, password):
    form_data = {
        'username': 'admin',
        'password': password,
        'csrftoken': login_token['csrftoken'],
        'timestamp': login_token['timestamp']

    }
    payload = urlencode(form_data)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    resp = req.post(base_url + '/admin',
                    headers=headers, data=payload)
    resp_headers = resp.request.headers
    return {'Cookie': resp_headers['Cookie']}
