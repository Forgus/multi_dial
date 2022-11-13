from router import Router
import time
import requests as req
import json
import getpass

url = "http://192.168.1.1/Action/call"
host = input("Router's host(192.168.1.1):")
if len(host) == 0:
    host = '192.168.1.1'
if ':' in host:
    host = host.split(':')[0]

pwd = getpass.getpass(prompt="admin@" + host + "'s password:")
ros = Router(pwd, host)
dial_info = ros.get_dial_info()
multi_pppoe_status = dial_info['status']

print('多拨配置: ')
print('绑定接口 拨号账号 拨号个数')
print(dial_info['interface'] + ' ' +
      dial_info['username'] + ' ' + str(dial_info['dial_num']))
print('多拨状态: ' + multi_pppoe_status)

restart_num = 0
# while (multi_pppoe_status != 'Success'):
#    dial_info = ros.get_dial_info()
#    success_list = dial_info['success_list']
#    success_num = len(success_list)
#    if success_num != 0:
#        print('成功个数: ', success_num, '失败个数: ',
#              len(dial_info['fail_list']), '重拨...')
#        ros.macvlan_down()
#        print("sleep 10 seconds to wait iface shutdown...")
#        time.sleep(10)
#    restart_num = restart_num + 1
#    print("restart macvlan...restart num: %d" % (restart_num))
#    ros.macvlan_up()
#    print("sleep 10 seconds to wait macvlan restart...")
#    time.sleep(10)
#    multi_pppoe_status = ros.get_dial_info()['status']
#    wait_times = 1
#    while (multi_pppoe_status == 'Pending' and wait_times <= 60):
#        print("wait more 10 seconds to pppoe connect...wait_times:%d" %
#              (wait_times))
#        time.sleep(10)
#        multi_pppoe_status = ros.get_dial_info()['status']
#        wait_times = wait_times + 1
