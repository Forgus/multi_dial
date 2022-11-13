import time
import requests as req
import json

url = "http://192.168.1.1/Action/call"


def macvlan_down():
    payload = json.dumps({
        "action": "vlan_down",
        "func_name": "wan",
        "param": {
            "id": "1,2,3,4,5"
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'sess_key=cd07c022f29a608dc9eb40376e5a1b41'
    }
    resp = req.request("POST", url, headers=headers, data=payload)
    print("macvlan_down,result:" + resp.text)


def macvlan_up():
    payload = json.dumps({
        "action": "vlan_up",
        "func_name": "wan",
        "param": {
            "id": "1,2,3,4,5"
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'sess_key=cd07c022f29a608dc9eb40376e5a1b41'
    }
    resp = req.request("POST", url, headers=headers, data=payload)
    print('macvlan_up result:' + resp.text)


success_list = []


def get_multi_pppoe_status():
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
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'sess_key=cd07c022f29a608dc9eb40376e5a1b41'
    }
    resp = req.request("POST", url, headers=headers, data=payload)
    success_num = 0
    enabled = ''
    for iface in resp.json()['Data']['vlan_data']:
        enabled = iface['enabled']
        ip_addr = iface['pppoe_ip_addr']
        if len(ip_addr) != 0:
            success_num += 1
            success_list.append(iface['vlan_name'])
    print('success adsl: ' + str[success_list])
    if success_num == 5:
        return 'Success'
    elif success_num == 0 and enabled == 'yes':
        return 'Pending'
    return 'Failed'


multi_pppoe_status = get_multi_pppoe_status()
print('multi_pppoe_status: ' + multi_pppoe_status)
# macvlan_down()
# macvlan_up()
restart_num = 0
while (multi_pppoe_status != 'Success'):
    macvlan_down()
    print("sleep 10 seconds to wait iface shutdown...")
    time.sleep(10)
    restart_num = restart_num + 1
    print("restart macvlan...restart num: %d" % (restart_num))
    macvlan_up()
    print("sleep 10 seconds to wait macvlan restart...")
    time.sleep(10)
    multi_pppoe_status = get_multi_pppoe_status()
    wait_times = 1
    while (multi_pppoe_status == 'Pending' and wait_times <= 60):
        print("wait more 10 seconds to pppoe connect...wait_times:%d" %
              (wait_times))
        time.sleep(10)
        multi_pppoe_status = get_multi_pppoe_status()
        wait_times = wait_times + 1
