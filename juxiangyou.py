import sys, threading, time, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
import requests, json
from bs4 import BeautifulSoup


class Main_win(QWidget):
    def __init__(self):
        super(Main_win, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('juxiangyou Window')
        self.setGeometry(100, 100, 200, 150)
        self.name = QLineEdit()
        self.password = QLineEdit()
        self.vali = QLineEdit()
        self.sub_button = QPushButton()
        self.sub_button.clicked.connect(self.submit_site)
        # self.password.setEchoMode(2)
        self.label = QLabel()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.photo = QPixmap()
        self.header = {
            "Accept": "text/html, application/xhtml+xml, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN",
            "Connection": "Keep-Alive",
            "Host": "www.juxiangyou.com",
            "Referer": "http://www.juxiangyou.com/",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64;Trident/5.0)"
        }
        url_1 = 'http://www.juxiangyou.com/login/index'
        req_1 = requests.get(url_1, headers=self.header)
        print(req_1.cookies.values())
        url_2 = 'http://www.juxiangyou.com/verify'
        req_2 = requests.get(url_2, headers=self.header, cookies=req_1.cookies)
        print(req_2.cookies.values())
        req_2.cookies.update(req_1.cookies)
        self.reqcookies = req_2.cookies
        print(self.reqcookies)
        self.photo.loadFromData(req_2.content)
        self.label.setPixmap(self.photo)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.vali)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.sub_button)

    def baseN(self, num, b):
        return ((num == 0) and "0") or (
            self.baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

    def submit_site(self):
        base_time = int(time.time()) * 1000
        x_sign = self.baseN(base_time, 36)
        post_head = {"Accept": "application/json, text/javascript, */*; q=0.01",
                     "Accept-Encoding": "gzip, deflate",
                     "Accept-Language": "zh-cn",
                     "Cache-Control": "no-cache",
                     "Connection": "Keep-Alive",
                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "Host": "www.juxiangyou.com",
                     "Referer": "http://www.juxiangyou.com/login/index",
                     "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
                     "X-Requested-With": "XMLHttpRequest"}
        try:
            # print('x_sign:' + x_sign + 's:' + self.s.cookies)
            post_head['X-Sign'] = x_sign
            a = json.dumps({"c": "index", "fun": "login", "account": self.name.text().strip(),
                            "password": self.password.text().strip(),
                            "verificat_code": self.vali.text().strip(),
                            "is_auto": 'false'})
            pst_data = {'jxy_parameter': a, 'timestamp': base_time}

            print(post_head)
            print(pst_data)
            url = 'http://www.juxiangyou.com/login/auth'
            self.req = requests.post(url, data=pst_data, cookies=self.reqcookies, headers=post_head,
                                     allow_redirects=False)
            print(self.req.content)
        except Exception as e:
            print(repr(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Main_win()
    mw.show()
    sys.exit(app.exec_())
