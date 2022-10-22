import pymysql


class RequestDAO:
    def __init__(self):
        self.name = "hihi"
        self.conn = RequestDAO.get_connection()

    def close(self):
        RequestDAO.close_connection(self)

    def fetch_all_requests(self):
        cur = self.conn.cursor()
        cur.execute("select * from ride_share_request_database.requests")
        output = cur.fetchall()
        return output

    def fetch_request_by_id(self, request_id):
        cur = self.conn.cursor()
        sql = "select * from ride_share_request_database.requests where request_id=%s"
        cur.execute(sql, args=request_id)
        result = cur.fetchone()
        return result

    def fetch_participants_by_request_id(self, request_id):
        cur = self.conn.cursor()
        sql = "select * from ride_share_request_database.participants where request_id=%s"
        cur.execute(sql, args=request_id)
        result = cur.fetchall()
        return result

    def create_request(self, info):
        pass

    @staticmethod
    def get_connection():
        print("hahaha")
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

if __name__ == "__main__":
    #print(RequestDAO.get_connection())
    dao = RequestDAO()
    out = dao.fetch_request_by_id(1)
    print(out)