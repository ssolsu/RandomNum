import sqlite3, os


class Sqlite_db:
    def create_db(self,name):
        try:
            conn = sqlite3.connect('pc16.db')
            # 可以检查是否有表，如果有表则先删除，再创建
            create_table_sql = '''CREATE TABLE pc16 (
                                          period varchar(20) NOT NULL UNIQUE,
                                          vote_time varchar(20) NOT NULL,
                                          jcjg1 varchar(20) NOT NULL,
                                          jcjg2 varchar(20) NOT NULL,
                                          state varchar(20) NOT NULL
                                        )'''
            conn.execute(create_table_sql)
            conn.commit()
            print("Table created successfully")
            conn.close()
        except Exception as e:
            print(repr(e))

    def get_conn(self):
        conn = ''
        if os.path.exists('pc16.db'):
            conn = sqlite3.connect('pc16.db')
        else:
            self.create_db('pc16.db')
        return conn

    def update_db(self, sql):
        result = False
        if os.path.exists('pc16.db'):
            conn = sqlite3.connect('pc16.db')
            try:
                conn.execute(sql)
                conn.commit()
                result = True
                print('更新成功')
            except Exception as e:
                print('重复更新失败',repr(e))
        return result

    def fetch(self, sql):
        result = ''
        if os.path.exists('pc16.db'):
            conn = sqlite3.connect('pc16.db')
            result = conn.execute(sql)
            conn.commit()
            print('查询完成')
            self.close_all(conn)
        else:
            self.create_db('pc16.db')
        return result

    def close_all(self, conn):
        try:
            if conn is not None:
                conn.close
        finally:
            if conn is not None:
                conn.close


if __name__ == "__main__":
    db = Sqlite_db()
    db.create_db()
