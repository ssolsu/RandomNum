import pyodbc,os
class DataBase:
    def __init__(self, dbname=None, dbhost=None):
        # 初始化，直接连接
        self._conn = self.connect_access()
        if self._conn:
            self._cursor = self._conn.cursor()
        sql = 'SELECT * from t1'
        rows=self.fetch_all(sql)
        print(rows[0])

    def connect_access(self):
        data_path = os.getcwd() + "\pceggs.accdb"
        odbc_path = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;UID=;PWD=" % data_path
        conn = False
        try:
            conn = pyodbc.connect(odbc_path)
            return conn
        except Exception as e:
            print(repr(e))
            return conn

    def fetch_all(self, sql):
        # 查询数据库
        res = ''
        if self._conn:
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchall()
            except Exception as data:
                print(repr(data))
                data = False
            return res