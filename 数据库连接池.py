#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
数据库连接池
Redis & MySQL
pip3 install DBUtils==2.0.1
"""
import pymysql
from dbutils.pooled_db import PooledDB
from rediscluster import RedisCluster


STARTUP_NODES = [                                   # 集群
        {"host": "10.10.100.101", "port": 7001},    # 主
        {"host": "10.10.100.102", "port": 7002},    # 从
        {"host": "10.10.100.103", "port": 7003},    # 主
        {"host": "10.10.100.104", "port": 7004},    # 从
        {"host": "10.10.100.105", "port": 7005},    # 主
        {"host": "10.10.100.106", "port": 7006}     # 从
    ]
pwd = '秘密不能告诉你'


class RedisConnPools(object):
    """Redis连接池"""
    __poll = None

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = self.__getConn()
        return self

    def __getConn(self):
        if self.__poll is None:
            # 连接单数据库
            # self.__poll = redis.ConnectionPool(
            #     host=host,
            #     port=port,
            #     db=db,
            #     password=pwd,
            #     max_connections=10
            # )

            # 连接redis集群, 构建StrictRedisCluster对象
            self.__poll = RedisCluster(
                startup_nodes=STARTUP_NODES,
                decode_responses=True,
                password=pwd,
                max_connections=300
            )

        return self.__poll

    def get_conn(self):
        conn = self.__getConn()
        return conn


class DBConnPools(object):
    """MySQL连接池"""
    __poll = None

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = self.__getConn()
        self.cursor = self.conn.cursor()
        return self

    def __getConn(self):
        if self.__poll is None:
            self.__poll = PooledDB(
                creator=pymysql,
                mincached=10,
                maxcached=10,
                maxshared=0,
                maxconnections=20,
                blocking=True,
                maxusage=5,
                ping=1,
                setsession=None,
                host='localhost',
                port=3306,
                user='user',
                passwd=pwd,
                db='db_1',
                use_unicode=True,
                charset='utf8'
            )
        return self.__poll.connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def get_conn(self):
        conn = self.__getConn()
        return conn


