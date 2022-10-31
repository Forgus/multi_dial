import requests as req


class Interface():

    def __init__(self, base_url, headers, type):
        self.iface_list = []
        self.success_list = []
        self.fail_list = []
        self.type = type
        self.base_url = base_url
        self.headers = headers

    def fetch_status(self):
        check_status_url = self.base_url + \
            "/admin/network/iface_status?type=" + self.type
        resp = req.get(check_status_url, headers=self.headers)
        for iface in resp.json():
            ifname = iface["ifname"]
            if '-' in ifname:
                wan_name = ifname.split('-')[1]
                self.success_list.append(wan_name)
                self.iface_list.append(wan_name)
            else:
                self.fail_list.append(ifname)
                self.iface_list.append(ifname)
        if len(self.success_list) == 0:
            self.multi_pppoe_status = 'Pending'
        if len(self.success_list) == len(self.iface_list):
            self.multi_pppoe_status = 'Success'
        else:
            self.multi_pppoe_status = 'Failed'
        return self.multi_pppoe_status

    def update_status(self):
        self.success_list.clear()
        self.fail_list.clear()
        return self.fetch_status()


class VirtualInterface(Interface):

    def __init__(self, base_url, headers, type='virtual'):
        super().__init__(base_url, headers, type)
