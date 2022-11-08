import requests as req


class Interface():

    def __init__(self, base_url, headers, type):
        self.type = type
        self.base_url = base_url
        self.headers = headers
        self.iface_num = self.get_iface_num()
        self.success_list = []
        self.fail_list = []

    def get_iface_num(self):
        check_status_url = self.base_url + \
            "/admin/network/iface_status?type=" + self.type
        resp = req.get(check_status_url, headers=self.headers)
        return len(resp.json())

    def fetch_status(self):
        check_status_url = self.base_url + \
            "/admin/network/iface_status?type=" + self.type
        resp = req.get(check_status_url, headers=self.headers)
        iface_list = resp.json()
        success_list = []
        fail_list = []
        for iface in iface_list:
            ifname = iface["ifname"]
            if '-' in ifname:
                wan_name = ifname.split('-')[1]
                success_list.append(wan_name)
            else:
                fail_list.append(ifname)
        self.success_list = success_list
        self.fail_list = fail_list
        success_num = len(success_list)
        if success_num == 0:
            return 'Pending'
        if success_num == self.iface_num:
            return 'Success'
        return 'Failed'


class VirtualInterface(Interface):

    def __init__(self, base_url, headers, type='virtual'):
        super().__init__(base_url, headers, type)
