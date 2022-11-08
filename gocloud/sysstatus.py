import requests as req


class Interface():

    def __init__(self, base_url, headers, type):
        self.iface_num = self.fetch_iface_num()
        self.success_list = []
        self.fail_list = []
        self.type = type
        self.base_url = base_url
        self.headers = headers

    def fetch_iface_num(self):
        check_status_url = self.base_url + \
            "/admin/network/iface_status?type=" + self.type
        resp = req.get(check_status_url, headers=self.headers)
        return len(resp.json())

    def fetch_status(self):
        check_status_url = self.base_url + \
            "/admin/network/iface_status?type=" + self.type
        resp = req.get(check_status_url, headers=self.headers)
        iface_status = {}
        success_list = []
        fail_list = []
        for iface in resp.json():
            ifname = iface["ifname"]
            if '-' in ifname:
                wan_name = ifname.split('-')[1]
                success_list.append(wan_name)
            else:
                fail_list.append(ifname)
        iface_status['success_list', success_list]
        iface_status['fail_list', fail_list]
        return iface_status

    def update_status(self):
        iface_status = self.fetch_status()
        success_list = iface_status['success_list']
        success_num = len(success_list)
        if success_num == 0:
            self.multi_pppoe_status = 'Pending'
        if success_num == self.iface_num:
            self.multi_pppoe_status = 'Success'
        else:
            self.multi_pppoe_status = 'Failed'
        self.success_list = success_list
        self.fail_list = iface_status['fail_list']
        return self.multi_pppoe_status


class VirtualInterface(Interface):

    def __init__(self, base_url, headers, type='virtual'):
        super().__init__(base_url, headers, type)
