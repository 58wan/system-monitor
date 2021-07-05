# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/6/29 9:44
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, String, Float

db = SQLAlchemy()


class Base(db.Model):
    """基础数据库模型：提供id、创建时间、更新时间"""
    __abstract__ = True
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # 支持中文
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Host(Base):
    ip = Column(String(32), comment="IP地址")
    hostname = Column(String(32), comment="主机名")
    cpu = Column(Float, comment="CPU使用率")
    memory = Column(Float, comment="内存使用率")

    users: list = db.relationship("User", back_populates="host")
    disks: list = db.relationship("Disk", back_populates="host")

    def data(self):
        return {
            "ip": self.ip,
            "hostname": self.hostname,
            "cpu": self.cpu,
            "memory": self.memory,
            "users": [user.data() for user in reversed(self.users)],
            "disks": [disk.data() for disk in reversed(self.disks)]
        }


class User(Base):
    host_id = Column(Integer, db.ForeignKey("host.id"))

    username = Column(String(32), comment="用户名")
    state = Column(String(32), comment="状态")
    free_time = Column(String(32), comment="空闲时间")
    login_time = Column(DateTime, comment="登录时间")

    host = db.relationship("Host", back_populates="users")

    def data(self):
        return {
            "username": self.username,
            "state": self.state,
            "free_time": self.free_time,
            "login_time": self.login_time.strftime("%Y-%m-%d %H:%M:%S") if self.login_time else ""
        }


class Disk(Base):
    host_id = Column(Integer, db.ForeignKey("host.id"))

    device = Column(String(32), comment="磁盘名称")
    disk_id = Column(String(64), comment="磁盘ID")
    # type = Column(String(32), comment="磁盘类型")
    # percent = Column(Float, comment="磁盘使用率")
    status = Column(Integer, comment="状态")
    confirmed = Column(Integer, default=0, comment="被确认")

    host = db.relationship("Host", back_populates="disks")

    def data(self):
        return {
            "id": self.id,
            "device": self.device,
            # "type": self.type,
            # "percent": self.percent,
            "disk_id": self.disk_id,
            "status": self.status,
            "confirmed": self.confirmed
        }
