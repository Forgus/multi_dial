import requests as req
import time


class MultiDial():

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def shutdown_iface(self, ifname):
        shutdown_url = self.base_url + "/admin/network/iface_shutdown/" + ifname
        req.get(shutdown_url, headers=self.headers)
        print("shutdown pppoe: " + ifname)

    def restart_macvlan(self):
        restart_url = self.base_url + "/servicectl/restart/macvlan"
        resp = req.get(restart_url, headers=self.headers)
        print("restart macvlan result: " + resp.text)
