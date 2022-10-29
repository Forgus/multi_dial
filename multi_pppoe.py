#!/usr/bin/python3
import requests
import time

dail_num = 5
gateway = "http://192.168.1.1"
headers = {
    'Cookie': 'sysauth=fc2c49eb1e9321b86ac9cf4c9cbf1a6f'
}

multi_dail_fail = True
fail_set = set()
success_set = set()

def get_token():
    login_page_url = gateway + "/cgi-bin/webui/admin"
    resp = requests.get(login_page_url)
    print(resp.text)

def check_status():
    check_status_url = gateway + "/cgi-bin/webui/admin/network/iface_status?type=virtual"
    resp = requests.get(check_status_url, headers=headers)
    pppoe_list = resp.json()
    success_set.clear()
    fail_set.clear()
    for pppoe in pppoe_list:
        ifname = pppoe["ifname"]
        if '-' in ifname:
            success_set.add(ifname.split('-')[1])
        else:
            fail_set.add(ifname)
    print("success set:" + str(success_set))
    print("fail set:" + str(fail_set))
    if len(success_set) == 0:
        return -1
    if len(success_set) == dail_num:
        print("multi dail success,dail_num:%d"%(dail_num))
        return 1
    else:
        print("multi dail failed.")
        return 0

def shutdown_pppoe(ifname):
    shutdown_url = gateway + "/cgi-bin/webui/admin/network/iface_shutdown/" + ifname
    response = requests.get(shutdown_url, headers=headers)
    print("shutdown pppoe: " + ifname)

def restart_macvlan():
    restart_url = gateway + "/cgi-bin/webui/servicectl/restart/macvlan"
    resp = requests.get(restart_url,headers=headers)
    print("restart macvlan result: " + resp.text)

get_token()
multi_dail_failed = (check_status() != 1)
restart_num = 0
while(multi_dail_failed):
    if len(success_set) != 0:
        for ifname in success_set:
            shutdown_pppoe(ifname)
        print("sleep 30 seconds to wait pppoe shutdown...")
        time.sleep(30)
    restart_num = restart_num + 1
    print("restart macvlan...restart num: %d"%(restart_num))
    restart_macvlan()
    print("sleep 30 seconds to wait macvlan restart...")
    time.sleep(30)
    dail_result = check_status()
    wait_times = 1
    while(dail_result == -1 and wait_times <= 60):
        print("wait more 10 seconds to pppoe connect...wait_times:%d"%(wait_times))
        time.sleep(10)
        dail_result = check_status()
        wait_times = wait_times + 1
    multi_dail_failed = (dail_result != 1)
