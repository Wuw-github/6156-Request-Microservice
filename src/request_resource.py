import pymysql

import os


class RequestDAO:

    def __int__(self):
        self.conn = RequestDAO._get_connection()

    @staticmethod
    def _get_connection():

        conn = pymysql.connect(
            user="okcloud",
            password="okcloudokcloud",
            host="okcloud-requests-database.cw2ylftvdgpn.us-east-1.rds.amazonaws.com",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def close_connection(dao):
        dao.conn.close()


