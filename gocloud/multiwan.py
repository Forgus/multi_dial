import requests as req


class MultiDial():

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_macvlan_settings(self):
        resp = req.get(self.base_url +
                       '/admin/multiwan/macvlan/macvlan', headers=self.headers)
        return resp.json()

    def shutdown_iface(self, ifname):
        shutdown_url = self.base_url + "/admin/network/iface_shutdown/" + ifname
        req.get(shutdown_url, headers=self.headers)
        print("shutdown pppoe: " + ifname)

    def restart_macvlan(self):
        restart_url = self.base_url + "/servicectl/restart/macvlan"
        req.get(restart_url, headers=self.headers)
