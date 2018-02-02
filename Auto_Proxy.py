import sys, threading, time, os, requests, re
from bs4 import BeautifulSoup
import Sqlite_db, telnetlib
import Data_Base


class Auto_Proxy:
    def __init__(self):
        self.url = 'http://www.xicidaili.com/nn/1'
        self.header = {
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN',
            'Connection': 'Keep-Alive',
            'Host': 'www.xicidaili.com',
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
        }
        self.collect_data()

    def collect_data(self):
        s = requests.session()
        req = s.get(self.url, headers=self.header)
        soup = BeautifulSoup(req.text, 'lxml')
        tr_text = soup.find_all('tr')
        for stra in tr_text[1:40]:
            try:
                list_text = stra.contents
                # print(list_text)
                ip_address = list_text[3].string
                ip_port = list_text[5].string
                ip_location = list_text[7].find('a').string
                ip_type = list_text[11].string
                ip_anomyous = list_text[9].string
                ip_speed = (list_text[15].find('div', class_="bar")).attrs['title']
                a = re.search('秒', ip_speed).span()
                # print(ip_address, ip_port, ip_location, ip_anomyous, ip_type, ip_speed[:a[0]])
                if float(ip_speed[:a[0]]) < 1:
                    self.test_ip(ip_address, ip_port, ip_type, ip_location, ip_anomyous, ip_speed[:a[0]])
            except Exception as e:
                print(repr(e))

    def test_ip(self, ip_address, ip_port, ip_type, ip_location, ip_anomyous, ip_speed):
        try:
            ip_add = "http://" + ip_address + ":" + ip_port
            ip_adds = "https://" + ip_address + ":" + ip_port
            req = requests.get('http://icanhazip.com/', proxies={'http': ip_add, 'https': ip_adds}, timeout=5)
            # print(req.text+'a')
            # telnetlib.Telnet(ip_address, port=ip_port, timeout=3)
            print(req.text, ip_address)
        except:
            print('connect failed')
        else:
            # sql='insert into ip values(ip_address,ip_port,ip_location,ip_type,ip_anomyous,ip_speed)'
            if (req.text).strip() == ip_address.strip():
                print('数据一致')
                param = [ip_address, ip_port, ip_location, ip_anomyous, ip_type, ip_speed]
                sql1 = 'insert into ip values (%s,%s,%s,%s,%s,%s)'
                Sqlite_db.Sqlite_db().update_db(sql1,param)
            else:
                print('数据与预期不一致')

    def update_data(self, sql):
        db = Sqlite_db.Sqlite_db()
        db.update_db(sql)


if __name__ == "__main__":
    Auto_Proxy()
