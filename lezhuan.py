# -*- coding: utf-8 -*-
import sys, time, os, re
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QRadioButton, QHBoxLayout,
                             QGridLayout, QSpinBox)
from PyQt5.QtGui import QPixmap
import requests, json, traceback, configparser
from PyQt5.QtCore import QThread, Qt
from bs4 import BeautifulSoup
import random

requests.adapters.DEFAULT_RETRIES = 5
requests.keep_alive = False
vote_mode = 0  # 0中边模式，1大小模式
maxwrong = 0
multiple = []
firstflag_vote = ''
firstflag_time = ''
firstflag_jinbi = ''
todayfirstjinbi = 0


class Main_win(QWidget):
    def __init__(self):
        super(Main_win, self).__init__()
        # self.initUI()
        self.UI()
        # self.t1 = Thread()

    def initUI(self):
        self.setWindowTitle('Le')
        self.setGeometry(100, 100, 600, 150)
        self.name = QLineEdit('xfpf@sina.com')
        self.password = QLineEdit('匿名')
        self.vali = QLineEdit()
        self.sub_button = QPushButton()
        self.rb = QRadioButton('中边模式')
        self.rb1 = QRadioButton('大小模式')

        self.rb.toggled.connect(self.change_vote_mode)
        self.rb.toggled.connect(self.change_vote_mode)
        self.sub_button.clicked.connect(self.submit_site)
        # self.password.setEchoMode(2)
        self.label = QLabel()
        self.label1 = QLabel()
        self.label2 = QLabel('当前金币：')
        self.label3 = QLabel()
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
        self.layout.addWidget(self.rb)
        self.layout.addWidget(self.rb1)
        self.layout.addWidget(self.label1)
        self.label1.setText('投注模式为：' + str(vote_mode))
        self.layout.addWidget(self.sub_button)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)
        self.rb.setChecked(True)
        global maxwrong
        maxwrong = 8
        global multiple
        multiple = [0, 1, 3, 7, 15, 31, 63, 127, 255, 1, 1, 1, 1, 1]

    def UI(self):
        self.setWindowTitle('LeZhuan')
        self.setGeometry(100, 100, 600, 150)
        self.all_layout = QHBoxLayout()  # 总布局为水平布局
        self.hlayout = QHBoxLayout()  # 局部布局（4个）：水平、竖直、网格、表单
        self.vlayout = QVBoxLayout()
        self.glayout = QGridLayout()
        # 设置左边部分登录部分的空间
        self.logo_lable = QLabel()
        self.logo_pic = QPixmap('lezhuan.png')
        self.logo_lable.setPixmap(self.logo_pic)
        self.name_label = QLabel('账户：')
        self.name_input = QLineEdit('xfpf@sina.com')
        self.password_lable = QLabel('密码：')
        self.password_input = QLineEdit('匿名')
        self.vali_lable = QLabel('验证码：')
        self.vali_input = QLineEdit()
        self.sub_button = QPushButton('登     录')
        self.sub_button.clicked.connect(self.submit_site)
        # 为左边网格布局添加图片等部件
        self.glayout.setSpacing(5)
        self.glayout.addWidget(self.logo_lable, 1, 0, 1, 0, Qt.AlignCenter)
        self.glayout.addWidget(self.name_label, 2, 0)
        self.glayout.addWidget(self.name_input, 2, 1)
        self.glayout.addWidget(self.password_lable, 3, 0)
        self.glayout.addWidget(self.password_input, 3, 1)
        self.glayout.addWidget(self.vali_lable, 4, 0)
        self.glayout.addWidget(self.vali_input, 4, 1)
        self.glayout.addWidget(self.sub_button, 5, 0, 1, 0)

        # 为右边的布局添加一个label来填充页面
        self.rightlable = QLabel('-----------------------------右布局预留空位---------------------')
        self.vlayout.addWidget(self.rightlable)
        # 准备2个部件
        vwg = QWidget()
        gwg = QWidget()

        # 2个部件设置局部布局
        vwg.setLayout(self.vlayout)
        gwg.setLayout(self.glayout)

        self.all_layout.addWidget(gwg)  # 2个部件加至全局布局
        self.all_layout.addWidget(vwg)
        self.setLayout(self.all_layout)

    def change_vote_mode(self):
        global vote_mode
        global maxwrong
        global multiple
        if self.rb.isChecked():
            vote_mode = 0
            maxwrong = 8
            multiple = [0, 1, 3, 7, 15, 31, 63, 127, 255, 1, 1, 1, 1, 1]
            self.label1.setText('投注模式为：' + str(vote_mode))
        elif self.rb1.isChecked():
            vote_mode = 1
            maxwrong = 11
            multiple = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 1, 1]
            self.label1.setText('投注模式为：' + str(vote_mode))

    def submit_site(self):
        global gol_cookies
        post_head = {"Accept": "application/json, text/javascript, */*; q=0.01",
                     "Accept-Encoding": "gzip, deflate",
                     "Accept-Language": "zh-cn",
                     "Cache-Control": "no-cache",
                     "Connection": "Keep-Alive",
                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "Host": "www.lezhuan.com",
                     "Referer": "http://www.lezhuan.com/login.html",
                     "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
                     "X-Requested-With": "XMLHttpRequest"}
        try:
            # 产生一个0-1的随机数字 17位
            rankey = random.random()
            # 直接发送请求ajax 获得token
            pst_ajax = {'act': 'visitReg', 'key': rankey, 'url': 'http://www.lezhuan.com/'}
            url = 'http://www.lezhuan.com/ajax.php'
            # Post数据服务器
            req = requests.post(url, data=pst_ajax, headers=post_head, allow_redirects=False)
            sub_ajax = {'act': 'login', 'key': rankey, 'url': 'http://www.lezhuan.com/',
                        'tbUserAccount': 'xfpf@sina.com', 'tbUserPwd': 'xfcctv1983',
                        'token': json.loads(req.text)['token']}
            time.sleep(0.1)
            req1 = requests.post(url, data=sub_ajax, headers=post_head, cookies=req.cookies, allow_redirects=False)
            if json.loads(req1.text)['error'] == '10000':
                print('登录成功')
                gol_cookies = req1.cookies
                return True
            else:
                return False
        except Exception as e:
            print(repr(e))


# 36进制转换公式方法
def baseN(num, b):
    return ((num == 0) and "0") or (
        baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def do_16():
    # 初始化判断是否错误,错误的次数
    # 初始化投注倍数
    jb = [3, 5, 8, 12]
    xxx = 1
    # 初始化投注期数
    global firstflag_vote
    global firstflag_jinbi
    wrong = 1
    vote_list = []
    header = {"Accept": "application/json, text/javascript, */*; q=0.01",
              "Accept-Encoding": "gzip, deflate",
              "Accept-Language": "zh-cn",
              "Cache-Control": "no-cache",
              "Connection": "Keep-Alive",
              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "Host": "www.lezhuan.com",
              "Referer": "http://www.lezhuan.com/login.html",
              "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
              "X-Requested-With": "XMLHttpRequest"}
    while True:
        vote_retime = 0
        current_period = ''
        list_v = []
        url = 'http://www.lezhuan.com/fun/'
        try:
            req = requests.get(url, cookies=gol_cookies, headers=header)
            soup = BeautifulSoup(req.text, 'lxml')
            # 查询当前投注信息
            vote_info = soup.findall('script', attrs={'type': 'text/javascript'})
            # 第一步 找到当前期 这里必然找出当前期，目的是为了投注。
            if vote_info != None:
                try:
                    temp_a = re.findall(r"parseInt\(\"(.+?)\"\)", vote_info[2].text)
                    temp_b = re.findall(r"fTimingNO = \"(.+?)\";", vote_info[2].text)
                    vote_current = int(temp_b[0])
                    vote_retime = int(temp_a[0])
                    if vote_retime > 9:
                        print('当前期' + vote_current + '剩余' + str(vote_retime) + '秒投注')
                    else:
                        print(vote_current,'截止投注')
                except Exception as e:
                    print('搜索资料出错，列表错误')
                    print('traceback.format_exc():%s' % traceback.format_exc())


                    # 如果没有开奖，则查询当前投注期

            # 找到当前期后，那么我们需要找到前4期，为投注准备,計算投注期，不需要時間也需要體現。

            if current_period != '':
                try:
                    current_jinbi = (soup.find('span', attrs={'class': 'J_udou'}).string).replace(',', '')
                except Exception as e:
                    print(repr(e))
                if firstflag_vote == '':
                    firstflag_vote = current_period
                    firstflag_jinbi = current_jinbi
                    config = configparser.ConfigParser()
                    config.read("Config.ini")
                    config_title = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    try:
                        config.add_section(config_title)
                        config.set(config_title, "starttime：", config_title)
                        config.set(config_title, "firstvote：", firstflag_vote)
                        config.set(config_title, "firstjinbi", firstflag_jinbi)
                        config.write(open("Config.ini", "w"))
                        tempa = config.sections()
                        newa = []
                        findtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                        # print(findtime)
                        for x in tempa:
                            # print(x.find(findtime))
                            if x.find(findtime) >= 0:
                                newa.append(x)
                        global todayfirstjinbi
                        todayfirstjinbi = int(config.get(newa[0], 'firstjinbi'))
                    except configparser.DuplicateSectionError:
                        print("Section already exists")
                if vote_list:  # 如果不为空，说明上一次投注了，判断是否正确。
                    vote_period = vote_list[-1]
                    last_vote = soup.find('td', text=vote_period).find_next_sibling('td', attrs={'class': 'num'}).find(
                        'span').string
                    print('返回列表', vote_list, '查找返回投注期的结果', last_vote)
                    if int(last_vote) in vote_list:
                        print('投注正确,倍率清空')
                        wrong = 1
                    else:
                        print('投注错误,次数加 1 ,错误次数：', wrong)
                        wrong = wrong + 1
                        if wrong >= maxwrong:
                            wrong = 1
                            xxx = xxx + 1
                            # 最大只能45倍
                            if xxx >= 3:
                                xxx = 3
                # 今日收益 等于 当前金币减掉今天第一次记录的金币数量
                temp = int(current_jinbi) - todayfirstjinbi
                yjshouru = jb[1] * 73 * 200
                if temp >= yjshouru:
                    xxx = 1
                    # 设定xxx为1，同时设置今日第一次金币数量为，当前的金币数量，开始第二轮
                    os._exit(0)
                s1 = str(int(current_period) - 1)
                s2 = str(int(current_period) - 2)
                s3 = str(int(current_period) - 3)
                s4 = str(int(current_period) - 4)
                last_1 = soup.find('td', text=s1).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
                last_2 = soup.find('td', text=s2).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
                last_3 = soup.find('td', text=s3).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
                last_4 = soup.find('td', text=s4).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
                temp_list = []
                for zz in range(1, 19):
                    temp1 = str(int(current_period) - zz)
                    z1 = soup.find('td', text=temp1).find_next_sibling('td', attrs={'class': 'num'}).find('span').string
                    temp_list.append(z1)
                if vote_mode == 0 and vote_retime > 9:
                    print('中边模式，最大错误次数:', maxwrong)
                    list_v = zhongandbian(last_1, last_2, multiple[wrong])
                if vote_mode == 1 and vote_retime > 9:
                    print('大小,最大错:', maxwrong, "当金币：", current_jinbi, '今收益', temp, '基倍', xxx, '预收',
                          str(yjshouru / 10000) + '万')
                    list_v = bigandmail(last_1, last_2, last_3, last_4, multiple[wrong], jb[xxx], temp_list)
                if list_v:
                    vote_list = vote_thing(current_period, list_v)
                else:
                    vote_list = []
            else:
                print('当前期都没找到，继续延时30秒查找')
                print(req.text)
            dealy_time = vote_retime + 28
            print('延时%s刷新,\n' % dealy_time)
            time.sleep(dealy_time)
        except Exception as e:
            print('访问网站出错，等待10秒，重新访问', repr(e))
            time.sleep(5)


# def bigandmail(s1, s2, s3, s4, multiple, bt):
#     # 该方法返回需要购买的列表
#     s1 = int(s1)
#     s2 = int(s2)
#     s3 = int(s3)
#     s4 = int(s4)
#     list_num = [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
#     if s1 > 7 and s1 < 14 and s1 < 11:  # 当前期为中小
#         # 判断假如不是中边中的情况，则直接跟中小
#         if (s2 < 8 or s2 > 13) and (s3 > 7 and s3 < 14):
#             # 中边中结构，跳过投注
#             print('中边中结构，跳过')
#             return []
#         elif s2 > 10 and s3 < 11:
#             for i in range(0, 8):
#                 list_num[i] = 0
#             list_num[8] = list_num[8] * bt * multiple
#             list_num[9] = list_num[9] * bt * multiple
#             list_num[10] = list_num[10] * bt * multiple
#             for i in range(11, 16):
#                 list_num[i] = 0
#             print('反转中大模式', list_num, '投注倍率:', multiple)
#             return list_num
#         else:
#             for i in range(0, 5):
#                 list_num[i] = 0
#             list_num[5] = list_num[5] * bt * multiple
#             list_num[6] = list_num[6] * bt * multiple
#             list_num[7] = list_num[7] * bt * multiple
#             for i in range(8, 16):
#                 list_num[i] = 0
#             print('投注中小模式,', list_num, '投注倍率:', multiple)
#             return list_num
#     elif s1 > 7 and s1 < 14 and s1 > 10:  # 当前期为中大
#         if (s2 < 8 or s2 > 13) and (s3 > 7 and s3 < 14):
#             # 中边中结构，跳过投注
#             print('中边中结构，跳过')
#             return []
#         elif s2 < 11 and s3 > 10:
#             # 符合大小大的结构，跳过投注
#             for i in range(0, 5):
#                 list_num[i] = 0
#             list_num[5] = list_num[5] * bt * multiple
#             list_num[6] = list_num[6] * bt * multiple
#             list_num[7] = list_num[7] * bt * multiple
#             for i in range(8, 16):
#                 list_num[i] = 0
#             # 那应该可以跟投中小
#             print('反转中小模式', list_num, '投注倍率:', multiple)
#             return list_num
#         else:
#             for i in range(0, 8):
#                 list_num[i] = 0
#             list_num[8] = list_num[8] * bt * multiple
#             list_num[9] = list_num[9] * bt * multiple
#             list_num[10] = list_num[10] * bt * multiple
#             for i in range(11, 16):
#                 list_num[i] = 0
#             # 那应该可以跟投中小
#             print('投注中大模式,投注倍率:', multiple)
#             return list_num
#     else:
#         print('不符合中大小模式')
#         return []


def bigandmail(s1, s2, s3, s4, multiple, bt, temp_list):
    # 该方法返回需要购买的列表
    vote_side = 0  # 0代表不投注，1代表投中小，2代表投中大
    side = 0  # 0代表上期为边，1代表是中边中，2代表正常，3代表反转
    s1 = int(s1)
    s2 = int(s2)
    s3 = int(s3)
    s4 = int(s4)
    list_num = [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
    if s1 > 7 and s1 < 14 and s1 < 11:  # 当前期为中小
        if (s2 < 8 or s2 > 13) and (s3 > 7 and s3 < 14):
            vote_side = 0
            side = 1
        else:
            if (s2 < 8 or s2 > 13) and (s3 < 8 or s3 > 13):
                # 中边边模式，直接反转
                vote_side = 2
                side = 3
            else:
                if s2 > 10 and s3 < 11:
                    # 小大小模式,反转
                    shibie = 0
                    if temp_list:
                        for index, item in enumerate(temp_list[3:-2]):
                            if int(item) < 11:
                                # 假如这期为小，那我们要看下一期和下二期是否能够组成小大小结构。
                                if int(temp_list[index + 4]) > 10 and int(temp_list[index + 5]) < 11:
                                    if int(temp_list[index + 2]) > 10:
                                        shibie = shibie + 1 / (index + 1)
                                    elif int(temp_list[index + 2]) < 11:
                                        shibie = shibie - 1 / (index + 1)
                    if shibie >= 0:
                        vote_side = 2
                        side = 3
                    else:
                        vote_side = 1
                        side = 3
                else:
                    vote_side = 1
                    side = 2
    if s1 > 7 and s1 < 14 and s1 > 10:  # 当前期为中大
        if (s2 < 8 or s2 > 13) and (s3 > 7 and s3 < 14):
            vote_side = 0
            side = 1
        else:
            if (s2 < 8 or s2 > 13) and (s3 < 8 or s3 > 13):
                # 中边边模式，直接反转，买中小
                vote_side = 1
                side = 3
            else:
                if s2 < 11 and s3 > 10:
                    # 大小大模式,反转，买中小
                    shibie = 0
                    if temp_list:
                        for index, item in enumerate(temp_list[3:-2]):
                            if int(item) > 10:
                                # 假如这期为大，那我们要看下一期和下二期是否能够组成大小大结构。
                                if int(temp_list[index + 4]) < 11 and int(temp_list[index + 5]) > 10:
                                    if int(temp_list[index + 2]) < 11:
                                        shibie = shibie + 1 / (index + 1)
                                    elif int(temp_list[index + 2]) > 10:
                                        shibie = shibie - 1 / (index + 1)
                    if shibie >= 0:
                        vote_side = 1
                        side = 3
                    else:
                        vote_side = 2
                        side = 3
                else:
                    vote_side = 2
                    side = 2
    if vote_side == 0 and side == 0:
        print('上期为边，直接跳过----')
        return []
    elif vote_side == 0 and side == 1:
        print('上期为中边中结构，直接跳过----')
        return []
    else:
        if vote_side == 1:
            for i in range(0, 5):
                list_num[i] = 0
            list_num[5] = list_num[5] * bt * multiple
            list_num[6] = list_num[6] * bt * multiple
            list_num[7] = list_num[7] * bt * multiple
            for i in range(8, 16):
                list_num[i] = 0
            if side == 2:
                print('正常投中小模式：', list_num, '投注倍率:', multiple)
            elif side == 3:
                print('反转小模式：', list_num, '投注倍率:', multiple)
            return list_num
        elif vote_side == 2:
            for i in range(0, 8):
                list_num[i] = 0
            list_num[8] = list_num[8] * bt * multiple
            list_num[9] = list_num[9] * bt * multiple
            list_num[10] = list_num[10] * bt * multiple
            for i in range(11, 16):
                list_num[i] = 0
            if side == 2:
                print('正常投中大模式：', list_num, '投注倍率:', multiple)
            elif side == 3:
                print('反转大模式：', list_num, '投注倍率:', multiple)
            return list_num


def zhongandbian(s1, s2, multiple):
    expend_list = []
    list_num = [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
    jb = 25
    s1 = int(s1)
    s2 = int(s2)
    return_list = []
    if s1 % 2 == 0 and s1 < 14 and s1 > 7 and s2 > 7 and s2 < 14:
        if s2 % 2 == 0 and s1 != s2:
            expend_list = [s2]
        # 上一期为中双，投注中单加上一期
        list_num[6] = list_num[6] * jb * multiple
        list_num[8] = list_num[8] * jb * multiple
        list_num[10] = list_num[10] * jb * multiple
        list_num[s1 - 3] = list_num[s1 - 3] * jb * multiple
        return_list = list_num
    elif s1 % 2 == 1 and s1 < 14 and s1 > 7 and s2 > 7 and s2 < 14:
        # 上一期为中单，投注中双加上一期
        if s2 % 2 == 1 and s1 != s2:
            expend_list = [s2]
        list_num[5] = list_num[5] * jb * multiple
        list_num[7] = list_num[7] * jb * multiple
        list_num[9] = list_num[9] * jb * multiple
        list_num[s1 - 3] = list_num[s1 - 3] * jb * multiple
        return_list = list_num
    if return_list:
        if expend_list:
            for x in expend_list:  # 扩张列表中是字符串格式
                list_num[x - 3] = list_num[x - 3] * jb * multiple
        print('中边模式，购买列表', return_list, "扩展列表", expend_list, '倍率:', multiple)
    else:
        print('中边模式，上期为边，跳过')
    return return_list


def vote_thing(vote_current, list_v):  # 负责投注的函数
    fpath = os.getcwd()
    return_list = []
    list_num = [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
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
                    "lotteryData": list_v})
    # 毫秒级时间戳，同时作为postdata数据发现服务器
    pst_data = {'jxy_parameter': a, 'timestamp': base_time}
    url = 'http://www.juxiangyou.com/fun/play/interaction'
    # Post数据服务器，cookies使用登录页面与验证码 合并cookies提交
    try:
        req = requests.post(url, data=pst_data, cookies=gol_cookies, headers=post_head,
                            allow_redirects=False, timeout=10)
        # print('打印投注返回信息:', req.text)
        vote_status = (json.loads(req.text))['code']
        if vote_status == 10000:
            # f = open(fpath + '\\a.txt', 'a+')
            # f.write(vote_current.strip() + " 列表：" + str(list_v) + "\n")
            # f.close()
            for x in range(0, 16):
                if list_v[x] > list_num[x]:
                    return_list.append(x + 3)
            return_list.append(vote_current.strip())
            print(vote_current, '投注成功购买的列表是', return_list)
            return return_list
        else:
            print(vote_current, '投注失败，购买的列表是空')
            return []
    except Exception as e:
        print('出错，购买的列表是空')
        return []


class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        try:
            do_16()
            # auto_data()
        except Exception as e:
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():%s' % traceback.format_exc())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Main_win()
    mw.show()
    sys.exit(app.exec_())
