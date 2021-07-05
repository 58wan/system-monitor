# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/6/29 9:17
import json

from flask import Flask, request
from flask_cors import CORS

from model import db, Host, User, Disk

app = Flask(__name__)
CORS(app, supports_credentials=True)

COUNTER = 0


@app.route("/monitor", methods=['POST'])
def monitor():
    global COUNTER
    data = request.json
    # print("data", data)
    ip = data['ip']
    hostname = data['hostname']
    cpu = data['cpu']
    memory = data['memory']
    users = data['users']
    disks = data['disks']

    host = db.session.query(Host).filter(Host.ip == ip).first()
    if host is None:
        host = Host()
        host.ip = ip
        host.hostname = hostname
        host.cpu = cpu
        host.memory = memory

        db.session.add(host)
    else:
        host.ip = ip
        host.hostname = hostname
        host.cpu = cpu
        host.memory = memory

    db.session.commit()

    for _user in users:
        username = _user['username']
        state = _user['state']
        free_time = _user['free_time']
        login_time = _user['login_time']
        """
        user = db.session.query(User).filter(User.host_id == host.id, User.username == username).first()
        if user is None:
            print("1111")
            user = User()
            user.host_id = host.id
            user.username = username
            user.state = state
            user.free_time = free_time
            user.login_time = login_time
            db.session.add(user)
        else:
            print("2222")
            user.host_id = host.id
            user.username = username
            user.state = state
            user.free_time = free_time
            user.login_time = login_time
            print(user)
            db.session.add(user.)
        """

        user = User()
        user.host_id = host.id
        user.username = username
        user.state = state
        user.free_time = free_time
        user.login_time = login_time
        COUNTER += 1
        if COUNTER > 99:
            COUNTER = 0
        if COUNTER % 5 == 0:
            print("user commit.")
            db.session.add(user)
            db.session.commit()

    for _disk in disks:
        device = _disk['device']
        disk_id = _disk['disk_id']
        status = _disk['status']
        confirmed = _disk['confirmed']

        disk = db.session.query(Disk).filter(Disk.host_id == host.id, Disk.device == device).first()
        if disk is None:
            disk = Disk()
            disk.host_id = host.id
            disk.device = device
            disk.disk_id = disk_id
            disk.status = status
            disk.confirmed = confirmed

            db.session.add(disk)
        else:
            disk.host_id = host.id
            disk.device = device
            disk.disk_id = disk_id
            disk.status = status
            disk.confirmed = confirmed
        db.session.commit()
    return "ok"


@app.route('/db_disks')
def get_disk_confirmed():
    # disk_id = request.form.get("disk_id")
    db_disks: Disk = db.session.query(Disk)
    data = [disk.data() for disk in db_disks]
    # return response(data=data)
    # if disk is None:
    #     return json.dumps(0, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def response(code=0, message='ok', **kwargs):
    """响应体数据格式"""
    data = {"code": code, "message": message}
    data.update(**kwargs)
    return data


@app.route('/disk_confirmed', methods=['PUT'])
def update_disk_confirmed():
    id = request.form.get("id")
    confirmed = request.form.get("confirmed")
    disk: Disk = db.session.query(Disk).filter(Disk.id == id).first()
    disk.confirmed = int(confirmed)
    if confirmed == "1":
        disk.status = 1
        db.session.merge(disk)
        db.session.commit()
    else:
        db.session.delete(disk)
        db.session.commit()
    return response(0, 'ok')


@app.route('/host')
def get_host_info():
    hosts = db.session.query(Host).all()

    data = []
    for host in hosts:
        data.append(host.data())
    return json.dumps({"code": 0,
                       "data": data
                       }, ensure_ascii=False)


def init_app():
    import config
    app.config.from_object(config)
    db.init_app(app)
    db.create_all(app=app)


if __name__ == '__main__':
    # os.environ["PG_USER"] = "postgres"
    # os.environ["PG_PASSWORD"] = "123456"
    # os.environ["PG_DB"] = "flask"
    # os.environ["PG_HOST"] = "172.18.77.18"
    # os.environ["PG_PORT"] = "20211"

    init_app()

    app.run(host="0.0.0.0", port='5000', debug=True)
