# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/6/29 9:19

# -------------------数据库配置-------------------
# 数据库配置：postgres
import os

JSON_AS_ASCII = False

PG_USER = os.getenv("PG_USER", "ent")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")
PG_DB = os.getenv("PG_DB", "postgres")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", 5432)
DB_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
SQLALCHEMY_DATABASE_URI = DB_URI
# -------------------数据库配置-------------------
