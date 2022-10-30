from router import Router
import time

ros = Router('')
multi_pppoe_status = ros.get_multi_pppoe_status()
print('multi_pppoe_status: ' + multi_pppoe_status)
restart_num = 0
while (multi_pppoe_status != 'Success'):
    success_list = ros.v_iface.success_list
    if len(success_list) != 0:
        for ifname in success_list:
            ros.shutdown_iface(ifname)
        print("sleep 30 seconds to wait iface shutdown...")
        time.sleep(30)
    restart_num = restart_num + 1
    print("restart macvlan...restart num: %d" % (restart_num))
    ros.restart_macvlan()
    print("sleep 30 seconds to wait macvlan restart...")
    time.sleep(30)
    multi_pppoe_status = ros.update_multi_pppoe_status()
    wait_times = 1
    while (multi_pppoe_status == 'Pending' and wait_times <= 60):
        print("wait more 10 seconds to pppoe connect...wait_times:%d" %
              (wait_times))
        time.sleep(10)
        multi_pppoe_status = ros.update_multi_pppoe_status()
        wait_times = wait_times + 1
