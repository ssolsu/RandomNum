# -*- coding: utf-8 -*-
import sys, time, os, Sqlite_16
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
import requests, json, traceback
from PyQt5.QtCore import QThread
from bs4 import BeautifulSoup


class Main_win(QWidget):
    def __init__(self):
        super(Main_win, self).__init__()
        self.initUI()
        self.t1 = Thread()

    def initUI(self):

        self.setWindowTitle('juxiangyou Window')
        self.setGeometry(100, 100, 200, 150)
        self.name = QLineEdit('ssolsu1@126.com')
        self.password = QLineEdit('xfcctv1983')
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
        # 通过访问登录界面返回Cookies访问验证码页面，然后合并提交cookies登录
        url_1 = 'http://www.juxiangyou.com/login/index'
        req_1 = requests.get(url_1, headers=self.header)
        # print(req_1.cookies.values())
        url_2 = 'http://www.juxiangyou.com/verify'
        req_2 = requests.get(url_2, headers=self.header, cookies=req_1.cookies)
        # print(req_2.cookies.values())
        req_2.cookies.update(req_1.cookies)
        self.reqcookies = req_2.cookies
        # print(self.reqcookies)
        # PyQt5 加载图片数据，访问验证码页面放回的byte格式数据
        self.photo.loadFromData(req_2.content)
        self.label.setPixmap(self.photo)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.vali)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.sub_button)

    def submit_site(self):
        global gol_cookies
        flag = False
        base_time = int(time.time()) * 1000
        x_sign = baseN(base_time, 36)
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
            # 为header字典添加一个X-sign标识，毫秒级时间戳36进制
            post_head['X-Sign'] = x_sign
            # 服务器接受str格式，把字典格式json格式转化
            a = json.dumps({"c": "index", "fun": "login", "account": self.name.text().strip(),
                            "password": self.password.text().strip(),
                            "verificat_code": self.vali.text().strip(),
                            "is_auto": 'false'})
            # 毫秒级时间戳，同时作为postdata数据发现服务器
            pst_data = {'jxy_parameter': a, 'timestamp': base_time}
            url = 'http://www.juxiangyou.com/login/auth'
            # Post数据服务器，cookies使用登录页面与验证码 合并cookies提交
            req = requests.post(url, data=pst_data, cookies=self.reqcookies, headers=post_head,
                                allow_redirects=False)

            if req.text.find('10000') > 0:
                print('登录成功，等待3秒，开始循环查询网页')
                # 登录成功，设定全局访问cookies
                gol_cookies = req.cookies
                flag = True
                # time.sleep(3)
                self.t1.start()
            elif req.text.find('10003') > 0:
                print('验证码或者密码错误')
            elif req.text.find('10005') > 0:
                print('密码输入错误，只有5次机会哦')
            else:
                print('莫名错误！！')
        except Exception as e:
            print(repr(e))
        return flag


# 36进制转换公式方法
def baseN(num, b):
    return ((num == 0) and "0") or (
        baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def do_16():
    # 初始化判断是否错误,错误的次数
    wrong = 1
    vote_list = []
    header = {
        "Accept": "text/html, application/xhtml+xml, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN",
        "Connection": "Keep-Alive",
        "Host": "www.juxiangyou.com",
        "Referer": "http://www.juxiangyou.com/",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64;Trident/5.0)"
    }
    while True:
        vote_retime = 0
        current_period = ''
        multiple = [0, 1, 3, 7, 15, 31, 63, 127, 255, 23, 26, 30, 34, 40]
        url = 'http://www.juxiangyou.com/fun/play/speed16/index'
        req = requests.get(url, cookies=gol_cookies, headers=header)
        soup = BeautifulSoup(req.text, 'lxml')
        tr_text = soup.find_all('tr', limit=12)
        # 查询当前投注信息
        vote_info = soup.find('label', attrs={'class': 'J_jcEnd'})
        # 判断是否刚好在开奖
        if (vote_info.text).find('正在开奖') > 0:
            print('正在开奖，等待5秒')
            time.sleep(5)
        else:
            # 如果没有开奖，则查询当前投注期
            try:
                vote_current = vote_info.find_all('span')
                # 结束标识，查询
                end_flag = (vote_info.text).find('截止投注')
                if end_flag > 0:
                    print(vote_current[0].string + '期已经截止投注')
                else:
                    print('当前期' + vote_current[0].string + '剩余' + vote_current[1].string + '秒投注')
                    vote_retime = int(vote_current[1].string)
                    current_period = vote_current[0].string
            except Exception as e:
                print('搜索资料出错，列表错误')
                print('traceback.format_exc():%s' % traceback.format_exc())
        # print(tr_text)
        # 手动查找上几期数据
        if current_period != '':
            s1 = str(int(current_period) - 1)
            s2 = str(int(current_period) - 2)
            s3 = str(int(current_period) - 3)
            s4 = str(int(current_period) - 4)
            last_1 = soup.find('td', text=s1).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
            last_result = int(last_1)
            last_2 = soup.find('td', text=s2).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
            last_3 = soup.find('td', text=s3).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
            last_4 = soup.find('td', text=s4).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
            expend_list = list(set([last_2, last_3, last_4]))
            print('上期期数:', s1, '开奖结果：', last_result, '多余列表', expend_list)
        if vote_list:  # 如果不为空，说明上一次投注了，判断是否正确。
            if last_result in vote_list:
                print('投注正确,倍率清空')
                wrong = 1
            else:
                print('投注错误,倍率+1')
                wrong = wrong + 1
        else:
            print('上期并没有投注,清空投注列表')

        if current_period != '' and last_result > 7 and last_result < 14:
            # 如果当前期不为空，并且可投注 投注
            # 这个部分还需要判断上一起是否为正确，如果不正确，倍数翻倍，如果正确，倍数归1---------
            pass
            # 复数
            if last_result % 2 == 0:
                # 投注中单
                # print('上期结果是中双')
                if (int(last_2) < 8 or int(last_2) > 13) or (int(last_3) < 8 or int(last_3) > 13):
                    print('上第二期或上第三期为边，直接跳过')
                else:
                    vote_list = vote_thing(current_period, last_result, 0, multiple[wrong], expend_list)

            elif last_result % 2 == 1:
                # 投注中双
                # print('上期结果是中单')
                if (int(last_2) < 8 or int(last_2) > 13) or (int(last_3) < 8 or int(last_3) > 13):
                    print('上第二期或上第三期为边，直接跳过')
                else:
                    vote_list = vote_thing(current_period, last_result, 0, multiple[wrong], expend_list)

        else:
            vote_list = []
            # print('上一期为边')
            # 不为中，是边，那判断上期我有投注吗？
            # 这个部分是考虑如何判断倍数问题
            pass
        dealy_time = vote_retime + 30
        print('延时%s刷新' % dealy_time)
        time.sleep(dealy_time)


def auto_data():
    post_head = {"Accept": "application/json, text/javascript, */*; q=0.01",
                 "Accept-Encoding": "gzip, deflate",
                 "Accept-Language": "zh-cn",
                 "Cache-Control": "no-cache",
                 "Connection": "Keep-Alive",
                 "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                 "Host": "www.juxiangyou.com",
                 "Referer": "http://www.juxiangyou.com/fun/play/speed16/index",
                 "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
                 "X-Requested-With": "XMLHttpRequest"}

    sq16 = Sqlite_16.Sqlite_db()
    conn = sq16.get_conn()
    for x in range(1, 45):
        try:
            base_time = int(time.time()) * 1000
            x_sign = baseN(base_time, 36)
            # 为header字典添加一个X-sign标识，毫秒级时间戳36进制
            post_head['X-Sign'] = x_sign
            # 服务器接受str格式，把字典格式json格式转化
            a = json.dumps({"c": "quiz", "fun": "getEachList", "items": "speed16", "pageSize": 23, "pageIndex": x})
            b = json.dumps({"items": "speed16"})
            # 毫秒级时间戳，同时作为postdata数据发现服务器
            pst_data = {'jxy_parameter': a, 'timestamp': base_time, 'params': b, 'xtpl': 'fun/private/jc-index-tbl'}
            url = 'http://www.juxiangyou.com/fun/play/interaction'
            # Post数据服务器，cookies使用登录页面与验证码 合并cookies提交
            req = requests.post(url, data=pst_data, cookies=gol_cookies, headers=post_head, allow_redirects=False)
            vote_data = json.loads(req.text)
            print(req.text)
            print(type(vote_data))
            if vote_data['code'] == 10000:
                print('数据反馈正常，开始循环查询')
                for x in vote_data['itemList']:
                    period = x['num']
                    vote_time = x['date']
                    jcjg1 = x['jcjg1']
                    jcjg2 = x['jcjg2']
                    state = x['state']
                    print(type(period), type(vote_time), type(jcjg1), type(jcjg2), type(state))
                    if state == 1:
                        print('已开奖期数', period)
                        sql = "insert into pc16 values ('" + period + "','" + vote_time + "','" + jcjg1 + "','" + str(
                            jcjg2) + "','" + str(state) + "')"
                        sq16.update_db(sql)
                    else:
                        print('没开奖期数', period)
        except Exception as e:
            print(repr(e))
        time.sleep(0.5)


def vote_thing(vote_current, last_result, sp_flag, multiple, expend_list):  # 负责投注的函数
    list_num = [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
    return_list = []
    if sp_flag == 0:  # 投注中单
        list_num[6] = list_num[6] * 50 * multiple
        list_num[8] = list_num[8] * 50 * multiple
        list_num[10] = list_num[10] * 50 * multiple
        list_num[last_result - 3] = list_num[last_result - 3] * 50 * multiple
        # print('投注买中单和上一期结果,倍数为:' + str(multiple))
        return_list = [9, 11, 13, last_result]
        for x in expend_list:
            print('x:', x)
            if int(x) < 8 or int(x) > 13:
                list_num[int(x) - 3] = list_num[int(x) - 3] * 50 * multiple
                return_list.append(int(x))


    else:  # 投注中双
        # print('投注买中单和上一期结果,倍数为:' + str(multiple))
        list_num[5] = list_num[5] * 50 * multiple
        list_num[7] = list_num[7] * 50 * multiple
        list_num[9] = list_num[9] * 50 * multiple
        list_num[last_result - 3] = list_num[last_result - 3] * 50 * multiple
        return_list = [8, 10, 12, last_result]
        for x in expend_list:
            print('x:', x)
            if int(x) < 8 or int(x) > 13:
                list_num[int(x) - 3] = list_num[int(x) - 3] * 50 * multiple
                return_list.append(int(x))
    print('经过修改后，投注的额度是列表是：', list_num, '倍率:', multiple)
    base_time = int(time.time()) * 1000
    x_sign = baseN(base_time, 36)
    post_head = {"Accept": "application/json, text/javascript, */*; q=0.01",
                 "Accept-Encoding": "gzip, deflate",
                 "Accept-Language": "zh-cn",
                 "Cache-Control": "no-cache",
                 "Connection": "Keep-Alive",
                 "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                 "Host": "www.juxiangyou.com",
                 "Referer": "http://www.juxiangyou.com/fun/play/speed16/jctz?id=" + vote_current,
                 "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
                 "X-Requested-With": "XMLHttpRequest"}
    post_head['X-Sign'] = x_sign
    # 服务器接受str格式，把字典格式json格式转化
    a = json.dumps({"fun": "lottery", "c": "quiz", "items": "speed16", "lssue": vote_current,
                    "lotteryData": list_num})
    # 毫秒级时间戳，同时作为postdata数据发现服务器
    pst_data = {'jxy_parameter': a, 'timestamp': base_time}
    url = 'http://www.juxiangyou.com/fun/play/interaction'
    # Post数据服务器，cookies使用登录页面与验证码 合并cookies提交
    try:
        req = requests.post(url, data=pst_data, cookies=gol_cookies, headers=post_head,
                            allow_redirects=False, timeout=10)
        # print('打印投注返回信息:', req.text)
        vote_status = json.loads(req.text)['code']
        if vote_status == '10000':
            print(vote_current + '投注成功')
        print('购买的列表是', return_list)
        return return_list
    except Exception as e:
        print('购买的列表是', return_list)
        return []


class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        try:
            auto_data()
        except Exception as e:
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():%s' % traceback.format_exc())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Main_win()
    mw.show()
    sys.exit(app.exec_())
