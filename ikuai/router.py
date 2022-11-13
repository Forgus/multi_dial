import login


class Router():

    def __init__(self, password, ip='192.168.1.1'):
        self.base_url = 'http://' + ip + '/Action'
        self.headers = login.login(
            self.base_url,  password)
        self.common_url = self.base_url + "/call"

    def get_dial_info(self):
        payload = json.dumps({
            "action": "show",
            "func_name": "wan",
            "param": {
                "ORDER": "asc",
                "ORDER_BY": "vlan_name",
                "TYPE": "vlan_data,vlan_total",
                "interface": "wan1",
                "limit": "0,20",
                "vlan_interface": 2
            }
        })
        resp = req.post(self.common_url, headers=self.headers, data=payload)
        enabled = ''
        resp_data = resp.json()['Data']
        dial_num = resp_data['vlan_total']
        success_list = []
        fail_list = []
        for iface in resp_data['vlan_data']:
            enabled = iface['enabled']
            ip_addr = iface['pppoe_ip_addr']
            vlan_name = iface['vlan_name']
            if len(ip_addr) != 0:
                success_list.append(vlan_name)
            else:
                fail_list.append(vlan_name)
            dial_info['interface'] = iface['interface']
            dial_info['username'] = iface['username']
        dial_info = {}
        dial_info['dial_num'] = dial_num
        dial_info['success_list'] = success_list
        dial_info['fail_list'] = fail_list
        success_num = len(success_list)
        if success_num == dial_num:
            dial_info['status', 'Success']
        elif success_num == 0 and enabled == 'yes':
            dial_info['status', 'Pending']
        else:
            dial_info['status', 'Failed']
        return dial_info

    def gen_id_str(num):
        id_str = str(list(range(1, num+1)))
        id_str = id_str.lstrip('[')
        id_str = id_str.rstrip(']')
        return id_str

    def macvlan_down(self, dial_num):
        payload = json.dumps({
            "action": "vlan_down",
            "func_name": "wan",
            "param": {
                "id": gen_id_str(dial_num)
            }
        })
        resp = req.post(self.common_url, headers=self.headers, data=payload)
        print("macvlan_down,result:" + resp.text)

    def macvlan_up(self, dial_num):
        payload = json.dumps({
            "action": "vlan_up",
            "func_name": "wan",
            "param": {
                "id": gen_id_str(dial_num)
            }
        })
        resp = req.post(self.common_url, headers=self.headers, data=payload)
        print('macvlan_up result:' + resp.text)
