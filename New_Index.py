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
        self.soup = BeautifulSoup(self.req_th.text, 'lxml')
        self.__VIEWSTATE = self.soup.find('input', attrs={'id': '__VIEWSTATE'}).get('value')
        self.__VIEWSTATEGENERATOR = self.soup.find('input', attrs={'id': '__VIEWSTATEGENERATOR'}).get('value')
        self.setLayout(self.layout)
        self.photo = QPixmap()
        self.photo.loadFromData(req_one.content)
        self.label.setPixmap(self.photo)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.vali)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.sub_button)

    def pc28(self):
        for n in range(13, 15):
            print("现在开始搜索第%d页" % n)
            url_pst = {'__VIEWSTATE': self.__VIEWSTATE,
                       '__VIEWSTATEGENERATOR': self.__VIEWSTATEGENERATOR,
                       'CurrentPageIndex': n,
                       'reloadshow': 11,
                       'soundshow': 10
                       }
            # print(self.__VIEWSTATE, self.__VIEWSTATEGENERATOR)
            url = "http://www.pceggs.com/play/pxya.aspx"
            url_req = requests.post(url, data=url_pst, cookies=self.req.cookies, headers=self.head_1)
            # print(url_req.text)
            self.soup = BeautifulSoup(url_req.text, 'lxml')
            tr_text = self.soup.find_all('tr', attrs={'align': 'center', 'bgcolor': '#FFFFFF'}, limit=20)
            # print(tr_text)
            for str in tr_text:
                try:
                    list_text = str.contents
                    betting_period = list_text[1].string
                    betting_time = list_text[3].string
                    betting_status = (list_text[15].string).split("'")[1]
                    betting_result = (list_text[5].string).split("'")[3]
                except (Exception)  as e:
                    print(repr(e))
                else:
                    print("投注期:" + betting_period, "投注时间:" + betting_time, "开奖结果:" + betting_result,
                          "开奖状态:" + betting_status)
            time.sleep(2)

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
        self.req.cookies.update(self.req_two.cookies)
        time.sleep(1)
        self.pc28()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Main_win()
    mw.show()
    sys.exit(app.exec_())
