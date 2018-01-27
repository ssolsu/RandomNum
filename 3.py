from bs4 import BeautifulSoup
import time,sys,re
import pyodbc


if __name__=='__main__':
    soup=BeautifulSoup(open('1.html'),'lxml')
    tr_text=soup.find_all('tr',attrs={'align':'center','bgcolor':'#FFFFFF'},limit=20)
    print(tr_text[5].contents)
    list_text=tr_text[0].contents
    betting_period=list_text[1].string
    betting_time=list_text[3].string
    betting_status=(list_text[15].string).split("'")[1]
    betting_result = (list_text[5].string).split("'")[3]
    print("投注期:"+betting_period,"投注时间:"+betting_time,"开奖结果:"+betting_result,"开奖状态:"+betting_status)
    for str in tr_text:
        list_text=str.contents
        betting_period = list_text[1].string
        betting_time = list_text[3].string
        betting_status = (list_text[15].string).split("'")[1]
        betting_result = (list_text[5].string).split("'")[3]
        print("投注期:" + betting_period, "投注时间:" + betting_time, "开奖结果:" + betting_result, "开奖状态:" + betting_status)
        time.sleep(1)
    def connet_database():
        conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=pceggs.accdb;Uid=;Pwd=;")
        cursor = conn.cursor()
        SQL = "SELECT * from table1;"
        for row in cursor.execute(SQL):
            print
            row.col1
        cursor.close()
        conn.close()
