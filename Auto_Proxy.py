import sys, threading, time, os, requests,re
from bs4 import BeautifulSoup


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

    def collect_data(self):
        s = requests.session()
        req = s.get(self.url, headers=self.header)
        soup = BeautifulSoup(req.text, 'lxml')
        tr_text=soup.find_all('tr')
        for str in tr_text[1:2]:
            list_text = str.contents
            print(list_text)
            ip_address = list_text[1].string
            print(ip_address)





if __name__ == "__main__":
    Auto_Proxy().collect_data()
