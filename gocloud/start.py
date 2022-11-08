from router import Router
import time
import getpass

url = input("Router's host(192.168.1.1):")
if len(url) == 0:
    url = '192.168.1.1'
if ':' in url:
    host = url.split(':')[0]
else:
    host = url
pwd = getpass.getpass(prompt="admin@" + host + "'s password:")
ros = Router(pwd, url)
multi_pppoe_status = ros.get_multi_pppoe_status()
macvlan_settings = ros.multi_dial.get_macvlan_settings()
config_list = macvlan_settings['tblsection']['list']


def get_config_value(config, key):
    return config['cbid.macvlan.cfg03b112.' + key]['value']


print('多拨配置: ')
print('绑定接口 备注 拨号账号 拨号密码 拨号个数')
for l in config_list:
    print(get_config_value(l, 'bind_if') + ' ' +
          get_config_value(l, 'remarks') + ' ' +
          get_config_value(l, 'username') + ' ' +
          get_config_value(l, 'password') + ' ' +
          get_config_value(l, 'dial_num') + ' ')
print('多拨状态: ' + multi_pppoe_status)
restart_num = 0
while (multi_pppoe_status != 'Success'):
    success_list = ros.v_iface.success_list
    success_num = len(success_list)
    if success_num != 0:
        print('成功个数:', success_num, '失败个数:',
              len(ros.v_iface.fail_list))
        print('重拨...')
        for ifname in success_list:
            ros.shutdown_iface(ifname)
        print("sleep 25 seconds to wait iface shutdown...")
        time.sleep(25)
    restart_num = restart_num + 1
    print("restart macvlan...restart times: %d" % (restart_num))
    ros.restart_macvlan()
    print("sleep 15 seconds to wait macvlan restart...")
    time.sleep(15)
    multi_pppoe_status = ros.get_multi_pppoe_status()
    wait_times = 1
    while (multi_pppoe_status == 'Pending' and wait_times <= 30):
        print("wait more 10 seconds to pppoe connect...wait_times:%d" %
              (wait_times))
        time.sleep(10)
        multi_pppoe_status = ros.get_multi_pppoe_status()
        print("多拨结果:" + multi_pppoe_status)
        wait_times = wait_times + 1
print('恭喜,', len(ros.v_iface.iface_list), '拨成功！')
