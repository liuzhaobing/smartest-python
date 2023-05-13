# -*- coding:utf-8 -*-
import logging

import pymongo
import pymysql

from main import DATABASE_CONFIG


class MySQL:
    def __init__(self, NAME: str, HOST: str, PORT: int, USER: str, PASSWORD: str, **kwargs):
        self.host = HOST
        self.port = PORT
        try:
            self.conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=NAME,
                                        charset='utf8', autocommit=True)
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 读取为列表+字典格式
            logging.info(f"connect to mysql success: {HOST}:{PORT}")
        except Exception as e:
            self.cursor = None
            self.conn = None
            logging.error(f"connect to mysql failed: {HOST}:{PORT} {e}")

    def __call__(self, query_string):
        try:
            self.cursor.execute(query_string)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"query to mysql failed: {query_string} {e}")
            return []

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            logging.error(f"disconnect to mysql failed: {self.host}:{self.port} {e}")


class MongoDB:
    def __init__(self, NAME: str, CLIENT: dict, **kwargs):
        uri = f"mongodb://{CLIENT['username']}:{CLIENT['password']}@{CLIENT['host']}:{CLIENT['port']}/{CLIENT['authSource']}"

        try:
            self.conn = pymongo.MongoClient(uri)
            self.db = self.conn[NAME]
            logging.info(f"connect to mongo success: {CLIENT['host']}:{CLIENT['port']}")
        except Exception as e:
            logging.error(f"connect to mongo failed: {CLIENT['host']}:{CLIENT['port']} {e}")
            self.conn = None
            self.db = None


if __name__ == '__main__':
    mysql = MySQL(**DATABASE_CONFIG.get("smartest_mysql"))
    result1 = mysql("select count(1) from skill_base_test;")
    print(result1)

    mongo = MongoDB(**DATABASE_CONFIG.get("smartest_mongo"))
    result2 = mongo.db["asr_filter_results"].count_documents({})
    print(result2)
