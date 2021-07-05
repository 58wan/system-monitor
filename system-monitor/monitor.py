import os
import socket
import sys
import time

import psutil
import requests


def get_host():
    # 获取本机电脑名
    hostname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    ip = socket.gethostbyname(hostname)

    return hostname, ip


def get_user():
    query_user = os.popen('query user')
    result = query_user.read()

    qu_list = result.split('\n')[1:-1]
    users = []
    for qu in qu_list:
        username = qu[0:22]
        free_time = qu[50:61]
        login_time = qu[61:]
        if username.startswith(">"):
            state = "当前用户"
        else:
            state = "已停用"
        username = username.lstrip(">")
        users.append({
            "username": username.strip(),
            "state": state.strip(),
            "free_time": free_time.strip(),
            "login_time": login_time.strip(),
        })
    return users


def get_disk(h_url):
    final_disks = []
    db_disks_id_list = []
    device = []
    for i in range(24):
        device.append("磁盘{}".format(i))
    disk_list = []
    disk_list_meta = os.popen('wmic diskdrive get serialnumber')
    result = disk_list_meta.read()
    disk_list_meta = result.split('\n')[1:-1]
    while '' in disk_list_meta:
        disk_list_meta.remove('')
    for disk in disk_list_meta:
        disk_list.append(disk.strip())
    db_disks = requests.get(h_url + ':5000/db_disks')
    db_disks = db_disks.json()

    if len(db_disks) == 0:
        i = 0
        for disk_id in disk_list:
            final_disks.append({
                "device": device[i],
                "disk_id": disk_id,
                "status": 1,
                "confirmed": 1,
            })
            i += 1
        return final_disks

    else:
        for disk in db_disks:
            # print(disk)     # <class 'dict'>
            db_disks_id_list.append(disk["disk_id"])

        lose = [x for x in db_disks_id_list if x not in disk_list]  # 在db_disks_id_list列表中而不在disk_list列表中
        new = [y for y in disk_list if y not in db_disks_id_list]  # 在disk_list列表中而不在db_disks_id_list列表中
        common = [val for val in db_disks_id_list if val in disk_list]

        # db_disks_id_list.extend(disk_list)
        # [all_list.append(i) for i in db_disks_id_list if not i in all_list]

        i = 0
        for disk in db_disks:
            if disk["disk_id"] in common:
                final_disks.append({
                    "device": device[i],
                    "disk_id": disk["disk_id"],
                    "status": disk["status"],
                    "confirmed": disk["confirmed"],
                })
            else:  # lose
                final_disks.append({
                    "device": device[i],
                    "disk_id": disk["disk_id"],
                    "status": -1,
                    "confirmed": 0,
                })
            i += 1
        for disk in new:
            final_disks.append({
                "device": device[i],
                "disk_id": disk,
                "status": 0,
                "confirmed": 0,
            })
            i += 1
        return final_disks


def monitor_info():
    h_url = "http://" + url
    hostname, ip = get_host()
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    users = get_user()
    disks = get_disk(h_url)

    data = {
        "ip": ip,
        "hostname": hostname,
        "cpu": cpu,
        "memory": memory,
        "users": users,
        "disks": disks
    }
    res = requests.post(h_url + ":5000/monitor", json=data)
    if res.status_code == 200:
        print("upload success")
    else:
        print('upload error')


def main():
    while 1:
        try:
            monitor_info()
        except Exception as e:
            print(e)
        # print(sleep_time)
        time.sleep(sleep_time)


if __name__ == '__main__':
    url = sys.argv[1]
    print("ip is ", url)
    print("port is ", "5000")

    sleep_time = int(sys.argv[2])
    main()