from router import Router
import time
import requests as req
import json
import getpass

login_addr = input("Router's login address(192.168.1.1):")
host = '192.168.1.1'
if ':' in login_addr:
    host = login_addr.split(':')[0]
elif len(login_addr) != 0:
    host = login_addr
pwd = getpass.getpass(prompt="admin@" + host + "'s password:")
iface_list = []
iface_str = input("Input interface(wan1):")
if len(iface_str) == 0:
    iface_list.append('wan1')
elif ',' in iface_str:
    iface_list = iface_str.split(',')
else:
    iface_list.append(iface_str)

target_num = input("Input your target dial num:")
if len(target_num) == 0:
    target_num = 5
else:
    target_num = int(target_num)
ros = Router(pwd, login_addr)
dial_info = ros.get_dial_info(target_num)
multi_pppoe_status = dial_info['status']


def get_id_list(dial_info):
    id_list = []
    for config in dial_info['config_list']:
        id_list.append(config['id'])
    return id_list


print('多拨配置: ')
print('名称 账号 密码 备注 IP')
for config in dial_info['config_list']:
    print(config['vlan_name'], config['username'], config['passwd'],
          config['comment'], config['ip_addr'])
print('总拨号个数:', dial_info['dial_num'], '预期成功个数:', target_num)
restart_num = 0
success_num = len(dial_info['success_list'])
while (multi_pppoe_status != 'Success'):
    dial_info = ros.get_dial_info(target_num)
    id_list = get_id_list(dial_info)
    success_list = dial_info['success_list']
    if len(success_list) != 0:
        print('成功线路: ', success_list, '失败线路: ',
              dial_info['fail_list'])
        time.sleep(5)
        print('停用所有线路...')
        ros.macvlan_down(id_list)
        print("sleep 15 seconds to wait macvlan shutdown...")
        time.sleep(15)
    restart_num = restart_num + 1
    print("重新尝试并发拨号，尝试次数: %d" % (restart_num))
    ros.macvlan_up(id_list)
    print("sleep 15 seconds to wait macvlan restart...")
    time.sleep(15)
    dial_info = ros.get_dial_info(target_num)
    multi_pppoe_status = dial_info['status']
    success_num = len(dial_info['success_list'])
    wait_times = 1
    while (multi_pppoe_status == 'Pending' and wait_times <= 60):
        print("wait more 10 seconds to pppoe connect...wait_times:%d" %
              (wait_times))
        time.sleep(10)
        multi_pppoe_status = ros.get_dial_info()['status']
        wait_times = wait_times + 1
print('恭喜!', success_num, '拨成功！')
