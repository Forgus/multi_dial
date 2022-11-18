import login
import json
import requests as req


class Router():

    def __init__(self, password, ip='192.168.1.1'):
        ip = '192.168.1.1' if len(ip) == 0 else ip
        self.base_url = 'http://' + ip + '/Action'
        self.headers = login.login(
            self.base_url,  password)
        self.common_url = self.base_url + "/call"

    def get_dial_result(self, iface):
        payload = json.dumps({
            "action": "show",
            "func_name": "wan",
            "param": {
                "ORDER": "asc",
                "ORDER_BY": "vlan_name",
                "TYPE": "vlan_data,vlan_total",
                "interface": iface,
                "limit": "0,20",
                "vlan_interface": 2
            }
        })
        return req.post(self.common_url, headers=self.headers, data=payload)

    def get_single_dial_info(self, iface):
        resp = self.get_dial_result(iface)
        enabled = 'no'
        resp_data = resp.json()['Data']
        success_list = []
        fail_list = []
        config_list = []
        for iface in resp_data['vlan_data']:
            enabled = iface['enabled']
            ip_addr = iface['pppoe_ip_addr']
            vlan_name = iface['vlan_name']
            if len(ip_addr) != 0:
                success_list.append(vlan_name)
            else:
                fail_list.append(vlan_name)
            config_info = {}
            config_info['id'] = iface['id']
            config_info['vlan_name'] = vlan_name
            config_info['username'] = iface['username']
            config_info['passwd'] = iface['passwd']
            config_info['ip_addr'] = ip_addr
            config_info['comment'] = iface['comment']
            config_info['enabled'] = '启用' if enabled == 'yes' else '停用'
            config_list.append(config_info)
        dial_info = {}
        dial_info['config_list'] = config_list
        dial_info['dial_num'] = resp_data['vlan_total']
        dial_info['success_list'] = success_list
        dial_info['fail_list'] = fail_list
        return dial_info

    def get_dial_info(self, iface_list, target_num):
        if len(iface_list) == 1:
            dial_info = self.get_single_dial_info(iface_list[0])
            success_num = len(dial_info['success_list'])
            if success_num >= target_num:
                dial_info['status'] = 'Success'
            elif success_num == 0:
                dial_info['status'] = 'Pending'
            else:
                dial_info['status'] = 'Failed'
            return dial_info
        if len(iface_list) == 2:
            info1 = self.get_single_dial_info(iface_list[0])
            info2 = self.get_single_dial_info(iface_list[1])
            s_list1 = info1['success_list']
            s_list2 = info2['success_list']
            dial_info = {}
            success_list = []
            for list in s_list1:
                success_list.append(list)
            for list in s_list2:
                success_list.append(list)
            fail_list = []
            for list in info1['fail_list']:
                fail_list.append(list)
            for list in info2['fail_list']:
                fail_list.append(list)
            config_list = []
            for list in info1['config_list']:
                config_list.append(list)
            for list in info2['config_list']:
                config_list.append(list)
            dial_info = {}
            dial_info['config_list'] = config_list
            dial_info['dial_num'] = info1['dial_num'] + info2['dial_num']
            dial_info['success_list'] = success_list
            dial_info['fail_list'] = fail_list
            success_num = len(s_list1) + len(s_list2)
            if success_num >= target_num and len(s_list1) > 0 and len(s_list2) > 0:
                dial_info['status'] = 'Success'
            elif success_num == 0:
                dial_info['status'] = 'Pending'
            else:
                dial_info['status'] = 'Failed'
            return dial_info
        return {}

    def gen_id_str(self, id_list):
        id_str = ''
        for id in id_list:
            id_str = id_str + str(id) + ','
        return id_str.rstrip(',')

    def macvlan_down(self, id_list):
        id_str = self.gen_id_str(id_list)
        payload = json.dumps({
            "action": "vlan_down",
            "func_name": "wan",
            "param": {
                "id": id_str
            }
        })
        req.post(self.common_url, headers=self.headers, data=payload)

    def macvlan_up(self, id_list):
        id_str = self.gen_id_str(id_list)
        payload = json.dumps({
            "action": "vlan_up",
            "func_name": "wan",
            "param": {
                "id": id_str
            }
        })
        req.post(self.common_url, headers=self.headers, data=payload)

    def add_dial_config(self, vlan_name, username, passwd, interface, comment=''):
        payload = json.dumps({
            "action": "vlan_add",
            "func_name": "wan",
            "param": {
                "vlan_name": vlan_name,
                "username": username,
                "passwd": passwd,
                "interface": interface,
                "comment": comment,
                "vlan_internet": 2
            }
        })
        req.post(self.common_url, headers=self.headers, data=payload)
