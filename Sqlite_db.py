import sqlite3, os


class Sqlite_db:
    DB_FILE_PATH = ''
    TABLE_NAME = ''
    SHOW_SQL = True

    def create_db(self):
        try:
            conn = sqlite3.connect('ip.db')
            # 可以检查是否有表，如果有表则先删除，再创建
            create_table_sql = '''CREATE TABLE ipnum (
                                          ip_address varchar(20) DEFAULT NULL,
                                          ip_port varchar(20) DEFAULT NULL,
                                          ip_location varchar(20) DEFAULT NULL,
                                          ip_anomyous varchar(20) DEFAULT NULL,
                                          ip_type varchar(20) DEFAULT NULL,
                                          ip_speed varchar(20) DEFAULT NULL
                                        )'''
            conn.execute(create_table_sql)
            conn.commit()
            print("Table created successfully")
            conn.close()
        except Exception as e:
            print(repr(e))

    def get_conn(self):
        conn = ''
        if os.path.exists('ip.db'):
            conn = sqlite3.connect('ip.db')
        else:
            self.create_db('ip.db')
        return conn

    def update_db(self, sql):
        result = False
        if os.path.exists('ip.db'):
            conn = sqlite3.connect('ip.db')
            conn.execute(sql)
            conn.commit()
            result = True
            print('更新成功')
        else:
            self.create_db('ip.db')
        return result

    def fetch(self, sql):
        result = ''
        if os.path.exists('ip.db'):
            conn = sqlite3.connect('ip.db')
            result = conn.execute(sql)
            conn.commit()
            print('查询完成')
            self.close_all(conn)
        else:
            self.create_db('ip.db')
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
