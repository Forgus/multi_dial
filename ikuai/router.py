import login
from sysstatus import VirtualInterface
from multiwan import MultiDial


class Router():

    def __init__(self, password, ip='192.168.1.1'):
        self.base_url = 'http://' + ip + '/Action'
        self.login_page = login.LoginPage(self.base_url)
        self.headers = login.login(
            self.base_url, self.login_page.login_token, password)
        self.v_iface = VirtualInterface(self.base_url, self.headers)
        self.multi_dial = MultiDial(self.base_url, self.headers)

    def get_multi_pppoe_status(self):
        return self.v_iface.fetch_status()

    def update_multi_pppoe_status(self):
        self.v_iface.update_status()

    def shutdown_iface(self, ifname):
        self.multi_dial.shutdown_iface(ifname)

    def restart_macvlan(self):
        self.multi_dial.restart_macvlan()
