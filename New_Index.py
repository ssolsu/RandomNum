import sys, threading, time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
import requests
from bs4 import BeautifulSoup


class Main_win(QWidget):
    def __init__(self):
        super(Main_win, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录窗口')
        self.setGeometry(100, 100, 200, 150)
        self.name = QLineEdit('ssolsu')
        self.password = QLineEdit('xfcctv1983')
        self.vali = QLineEdit()
        self.sub_button = QPushButton()
        self.sub_button.clicked.connect(self.submit_site)
        self.password.setEchoMode(2)
        self.label = QLabel()
        self.layout = QVBoxLayout()
        self.head_1 = {'Host': 'www.pceggs.com',
                       'Proxy-Connection': 'keep-alive',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) ',
                       'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                       'Referer': 'http://www.pceggs.com/nologin.aspx'
                       }
        # 使用该页面可以获得cookies,Cline_key,使用该cookies访问VerifyCode_Login.aspx，获得show_login key
        url_one = 'http://www.pceggs.com/VerifyCode_Login.aspx'
        req_one = requests.get(url_one, headers=self.head_1)
        url_two = 'http://www.pceggs.com/showlogin/VerifyCode_ShowLogin.aspx'
        self.req_two = requests.get(url_two, headers=self.head_1, cookies=req_one.cookies)
        self.req_two.cookies.update(req_one.cookies)
        self.url_three = 'http://www.pceggs.com/nologin.aspx'
        self.req_th = requests.get(self.url_three, headers=self.head_1, cookies=self.req_two.cookies)
        soup = BeautifulSoup(self.req_th.text, 'lxml')
        self.__VIEWSTATE = soup.find('input', attrs={'id': '__VIEWSTATE'}).get('value')
        self.__VIEWSTATEGENERATOR = soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'}).get('value')
        self.setLayout(self.layout)
        self.photo = QPixmap()
        self.photo.loadFromData(req_one.content)
        self.label.setPixmap(self.photo)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.vali)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.sub_button)

    def submit_site(self):
        pst_data = {'txt_UserName': self.name.text(), 'txt_PWD': self.password.text(), '__VIEWSTATE': self.__VIEWSTATE,
                    '__VIEWSTATEGENERATOR': self.__VIEWSTATEGENERATOR, 'txt_VerifyCode': self.vali.text(),
                    'Login_Submit.x': 42,
                    'Login_Submit.y': 26,
                    'SMONEY': 'ABC'
                    }
        url = 'http://www.pceggs.com/nologin.aspx'
        self.req = requests.post(url, data=pst_data, cookies=self.req_two.cookies, headers=self.head_1,
                            allow_redirects=False)
        print(self.name.text(), self.password.text(), self.__VIEWSTATE, self.__VIEWSTATEGENERATOR, self.vali.text())
        print(self.req.cookies)

    def pc28(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Main_win()
    mw.show()
    sys.exit(app.exec_())
