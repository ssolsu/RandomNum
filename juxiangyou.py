import sys, threading, time, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
import requests, Data_Base
from bs4 import BeautifulSoup


class Main_win(QWidget):
    def __init__(self):
        super(Main_win, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('juxiangyou登录窗口')
        self.setGeometry(100, 100, 200, 150)
        self.name = QLineEdit('ssolsu1@126.com')
        self.password = QLineEdit('xfcctv1983')
        self.vali = QLineEdit()
        self.sub_button = QPushButton()
        # self.sub_button.clicked.connect(self.submit_site)
        # self.password.setEchoMode(2)
        self.label = QLabel()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.photo = QPixmap()
        header = {
            "Accept": "text/html, application/xhtml+xml, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN",
            "Connection": "Keep-Alive",
            "Host": "www.juxiangyou.com",
            "Referer": "http://www.juxiangyou.com/",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64;Trident/5.0)"
        }
        s = requests.session()
        url_1 = 'http://www.juxiangyou.com/login/index'
        req_1 = s.get(url_1, headers=header)
        url_2 = 'http://www.juxiangyou.com/verify'
        req_2 = s.get(url_2, headers=header)
        self.photo.loadFromData(req_2.content)
        self.label.setPixmap(self.photo)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.vali)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.sub_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Main_win()
    mw.show()
    sys.exit(app.exec_())
