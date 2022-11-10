import pymysql


class RequestDAO:
    def __init__(self):
        self.conn = RequestDAO.get_connection()

    def close(self):
        RequestDAO.close_connection(self)

    def fetch_all_requests(self, args):
        cur = self.conn.cursor()
        sql = "select * from requests where (1=1)"
        if args.get('start'):
            sql += f" and (start_location='{args.get('start')}')"
        if args.get('destination'):
            sql += f" and (destination='{args.get('destination')}')"
        if args.get('time'):
            sql += f" and (start_time='{args.get('time')}')"
        cur.execute(sql)
        output = cur.fetchall()
        return output

    def fetch_request_by_id(self, request_id):
        cur = self.conn.cursor()
        sql = "select * from requests where request_id=%s"
        cur.execute(sql, args=request_id)
        result = cur.fetchone()
        return result

    def fetch_participants_by_request_id(self, request_id):
        cur = self.conn.cursor()
        sql = "select * from participants where request_id=%s"
        cur.execute(sql, args=request_id)
        result = cur.fetchall()
        return result

    def create_request(self, info, user_id):
        sql = "insert into requests" \
              "(launch_date, start_time, start_location, destination, description, capacity) " \
              "values (%s, %s, %s, %s, %s, %s)"

        cur = self.conn.cursor()
        cur.execute(sql, [info.date, info.time, info.start_loc, info.dest, info.description, info.capacity])

        request_id = cur.lastrowid
        self.create_participant(request_id, user_id)
        print("new request_id", request_id)

    def create_participant(self, request_id, user_id):
        sql = "insert into participants (request_id, user_id)" \
              "values (%s, %s)"
        cur = self.conn.cursor()
        cur.execute(sql, [request_id, user_id])

    def update_request(self, request_id, info):
        cur = self.conn.cursor()
        sql = """
            UPDATE requests
            SET launch_date=%s, start_time=%s, start_location=%s, destination=%s, description=%s, capacity=%s
            WHERE request_id=%s
              """
        cur.execute(sql, [info.date, info.time, info.start_loc, info.dest, info.description, info.capacity, request_id])

    def _delete_request(self, request_id):
        cur = self.conn.cursor()
        sql = "delete from requests where request_id=%s"
        cur.execute(sql, request_id)

    def delete_participant(self, request_id, user_id):
        cur = self.conn.cursor()
        sql = "delete from participants where request_id=%s and user_id=%s"
        cur.execute(sql, [request_id, user_id])

        participants = self.fetch_participants_by_request_id(request_id)
        if not participants:
            self._delete_request(request_id)

    @staticmethod
    def get_connection():
        print("hahaha")
        conn = pymysql.connect(
            user="hbstudent",
            password="hbstudent",
            host="localhost",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        conn.select_db('ride_share_request_database')
        return conn

    @staticmethod
    def close_connection(dao):
        dao.conn.close()


if __name__ == "__main__":
    # print(RequestDAO.get_connection())
    dao = RequestDAO()
    out = dao.fetch_request_by_id(1)
    print(out)
