from router import Router
import time
import requests as req
import json
import getpass
import paramiko
import os

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
dial_info = ros.get_dial_info(iface_list, target_num)
multi_pppoe_status = dial_info['status']


def get_id_list(dial_info):
    id_list = []
    for config in dial_info['config_list']:
        id_list.append(config['id'])
    return id_list


def start_task(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, "root", "1")
    execmd = 'docker start wxedge'
    ssh.exec_command(execmd)
    ssh.close()


def get_fail_id_list(dial_info):
    id_list = []
    fail_list = dial_info['fail_list']
    for config in dial_info['config_list']:
        if config['vlan_name'] in fail_list:
            id_list.append(config['id'])
    return id_list


print('多拨配置: ')
print('名称 账号 密码 备注 状态 IP')
for config in dial_info['config_list']:
    print(config['vlan_name'], config['username'], config['passwd'],
          config['comment'], config['enabled'], config['ip_addr'])
print('总拨号个数:', dial_info['dial_num'], '预期成功个数:', target_num)
restart_num = 0
success_num = len(dial_info['success_list'])
while (multi_pppoe_status != 'Success'):
    dial_info = ros.get_dial_info(iface_list, target_num)
    id_list = get_id_list(dial_info)
    success_list = dial_info['success_list']
    if len(success_list) != 0:
        print('成功线路: ', success_list, '失败线路: ',
              dial_info['fail_list'])
        time.sleep(5)
        print('停用所有线路...')
        ros.macvlan_down(id_list)
        print("sleep 30 seconds to wait macvlan shutdown...")
        time.sleep(30)
    restart_num = restart_num + 1
    print("重新尝试并发拨号，尝试次数: %d" % (restart_num))
    ros.macvlan_up(id_list)
    print("sleep 25 seconds to wait macvlan restart...")
    time.sleep(25)
    dial_info = ros.get_dial_info(iface_list, target_num)
    multi_pppoe_status = dial_info['status']
    success_num = len(dial_info['success_list'])
    wait_times = 1
    while (multi_pppoe_status == 'Pending' and wait_times <= 60):
        print("wait more 10 seconds to pppoe connect...wait_times:%d" %
              (wait_times))
        time.sleep(10)
        multi_pppoe_status = ros.get_dial_info(
            iface_list, target_num)['status']
        wait_times = wait_times + 1
print('恭喜!', success_num, '拨成功！')
print('成功线路: ', dial_info['success_list'], '失败线路: ',
      dial_info['fail_list'])
print('停用失败线路...')
fail_id_list = get_fail_id_list(dial_info)
ros.macvlan_down(fail_id_list)
print('停用成功.')
# print('启动所有任务')
#os.system('docker start wxedge')
# start_task('192.168.1.55')
# start_task('192.168.1.65')
# start_task('192.168.1.75')
# start_task('192.168.1.85')
# start_task('192.168.1.2')
