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
requests.keep_alive = True
vote_mode = 1  # 0中边模式，1大小模式
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
        self.t1 = Thread()

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
        multiple = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 1, 1]

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
        self.rb = QRadioButton('中边模式')
        self.rb1 = QRadioButton('大小模式')
        self.rb2 = QRadioButton('余数模式')
        self.rb.toggled.connect(self.change_vote_mode)
        self.rb1.toggled.connect(self.change_vote_mode)
        self.rb2.toggled.connect(self.change_vote_mode)
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
        self.glayout.addWidget(self.rb, 5, 0)
        self.glayout.addWidget(self.rb1, 5, 1)
        self.glayout.addWidget(self.rb2, 5, 2)
        self.glayout.addWidget(self.sub_button, 6, 0, 1, 0)

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
            # self.label1.setText('投注模式为：' + str(vote_mode))
        elif self.rb1.isChecked():
            vote_mode = 1
            maxwrong = 11
            multiple = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 1, 1]
            # self.label1.setText('投注模式为：' + str(vote_mode))
        elif self.rb2.isChecked():
            vote_mode = 2
            maxwrong = 11
            multiple = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 1, 1]

    def submit_site(self):
        global gol_cookies
        post_head = {"Accept": "application/json, text/javascript, */*",
                     "Accept-Encoding": "gzip, deflate",
                     "Accept-Language": "zh-cn",
                     "Cache-Control": "no-cache",
                     "Connection": "Keep-Alive",
                     "Content-Type": "application/x-www-form-urlencoded",
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
                cj_dict = requests.utils.dict_from_cookiejar(gol_cookies)
                cj_dict['cGlobal[last]'] = str(int(time.time()))
                gol_cookies = requests.utils.cookiejar_from_dict(cj_dict, cookiejar=None, overwrite=True)
                print(gol_cookies)
                self.t1.start()
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
    jb = [1, 2, 4, 8]
    xxx = 1
    mmode = 2
    # 初始化投注期数
    global firstflag_vote
    global firstflag_jinbi
    wrong = 1
    vote_list = []
    header = {"Accept": "application/json, text/javascript, */*",
              "Accept-Encoding": "gzip, deflate",
              "Accept-Language": "zh-cn",
              "Cache-Control": "no-cache",
              "Connection": "Keep-Alive",
              "Content-Type": "application/x-www-form-urlencoded",
              "Host": "www.lezhuan.com",
              "Referer": "http://www.lezhuan.com/",
              "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
              "X-Requested-With": "XMLHttpRequest"}
    while True:
        vote_retime = 0
        current_period = ''
        list_v = []
        url = 'http://www.lezhuan.com/fast/'
        try:
            gol_cookies['cGlobal[last]'] = str(int(time.time()))

            req = requests.get(url, cookies=gol_cookies, headers=header)
            # print('查询页面时使用的全局cookies', gol_cookies)
            soup = BeautifulSoup(req.text, 'lxml')
            # 查询当前投注信息
            vote_info = soup.find_all('script', attrs={'type': 'text/javascript'})
            # 第一步 找到当前期 这里必然找出当前期，目的是为了投注。
            if vote_info != None:
                try:
                    temp_a = re.findall(r"parseInt\(\"(.+?)\"\)", vote_info[2].text)
                    temp_b = re.findall(r"fTimingNO = \"(.+?)\";", vote_info[2].text)
                    current_period = temp_b[0]
                    vote_retime = int(temp_a[0])
                    if vote_retime > 9:
                        print('当前期' + current_period + '剩余' + str(vote_retime) + '秒投注')
                    else:
                        print(current_period, '截止投注')
                except Exception as e:
                    print('搜索资料出错，列表错误')
                    print('traceback.format_exc():%s' % traceback.format_exc())
                    # 如果没有开奖，则查询当前投注期
            # 找到当前期后，那么我们需要找到前4期，为投注准备,計算投注期，不需要時間也需要體現。
            if current_period != '':
                try:
                    current_jinbi = (
                        soup.find('span', attrs={'style': 'padding-left:10px;'}).find_next_sibling(
                            'span').string).replace(
                        ',', '')
                except Exception as e:
                    print(repr(e))
                if firstflag_vote == '':
                    firstflag_vote = current_period
                    firstflag_jinbi = current_jinbi
                    config = configparser.ConfigParser()
                    config.read("Config_lezhuan.ini")
                    config_title = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    try:
                        config.add_section(config_title)
                        config.set(config_title, "starttime：", config_title)
                        config.set(config_title, "firstvote：", firstflag_vote)
                        config.set(config_title, "firstjinbi", firstflag_jinbi)
                        config.write(open("Config_lezhuan.ini", "w"))
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
                    try:
                        vote_period = vote_list[-1]
                        temp1 = (soup.find('td', text=vote_period).find_next_siblings('td')[1].find_all('img'))[-1]
                        last_vote = re.findall(r'\d+', str(temp1))
                        print('返回列表', vote_list, '查找返回投注期的结果', last_vote[0])
                        if int(last_vote[0]) in vote_list:
                            print('投注正确,倍率清空')
                            wrong = 1
                        else:
                            if int(last_vote[0]) > 0:
                                print('投注错误,次数加 1 ,错误次数：', wrong)
                                wrong = wrong + 1
                                if wrong >= maxwrong:
                                    wrong = 1
                                    xxx = xxx + 1
                                    if xxx >= 3:
                                        xxx = 3
                    except Exception as e:
                        print(repr(e))
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
                temp_w = (soup.find('td', text=s1).find_next_siblings('td')[1].find_all('img'))[-1]
                last_1 = re.findall(r'\d+', str(temp_w))[0]
                temp_x = (soup.find('td', text=s2).find_next_siblings('td')[1].find_all('img'))[-1]
                last_2 = re.findall(r'\d+', str(temp_x))[0]
                temp_y = (soup.find('td', text=s3).find_next_siblings('td')[1].find_all('img'))[-1]
                last_3 = re.findall(r'\d+', str(temp_y))[0]
                temp_z = (soup.find('td', text=s4).find_next_siblings('td')[1].find_all('img'))[-1]
                last_4 = re.findall(r'\d+', str(temp_z))[0]
                temp_list = []
                for zz in range(1, 19):
                    temp1 = str(int(current_period) - zz)
                    z1 = (soup.find('td', text=temp1).find_next_siblings('td')[1].find_all('img'))[-1]
                    z2 = re.findall(r'\d+', str(z1))[0]
                    temp_list.append(z2)
                if vote_mode == 0 and vote_retime > 9:
                    print('中边模式，最大错误次数:', maxwrong)
                    list_v = zhongandbian(last_1, last_2, multiple[wrong])
                if vote_mode == 1 and vote_retime > 9:
                    print('大小,最大错:', maxwrong, "当金币：", current_jinbi, '今收益', temp, '基倍', xxx, '预收',
                          str(yjshouru / 10000) + '万')
                    list_v = bigandmail(last_1, last_2, last_3, last_4, multiple[wrong], jb[xxx], temp_list)
                    # print(last_1, last_2, last_3, last_4, multiple[wrong], jb[xxx], temp_list)
                if vote_mode == 2 and vote_retime > 9:
                    print('余数,最大错:', maxwrong, "当金币：", current_jinbi, '今收益', temp, '基倍', xxx, '预收',
                          str(yjshouru / 10000) + '万')
                    if wrong == 1:
                        print('错误为1,重新随机mmode', mmode)
                        mmode = random.randint(1, 3)
                    list_v = mod3_bm(last_1, last_2, last_3, last_4, multiple[wrong], jb[xxx], temp_list, mmode)
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


def mod3_bm(s1, s2, s3, s4, multiple, bt, temp_list, mmode):
    vote_side = 0  # 0代表不投注，1代表投中小，2代表投中大
    side = 0  # 0代表上期为边，1代表是中边中，2代表正常，3代表反转
    s1 = int(s1)
    s2 = int(s2)
    s3 = int(s3)
    s4 = int(s4)
    list_f = []
    list_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    list_num = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 63, 69, 73, 75, 75, 73, 69, 63, 55, 45, 36, 28, 21, 15, 10, 6, 3,
                1]
    if mmode == 1:
        # 取余数0,1
        a = 0
        b = 1
    elif mmode == 2:
        # 取余数0,2
        a = 0
        b = 2
    else:
        # 取余数1,2
        a = 1
        b = 2
    if s1 % 3 == a or s1 % 3 == b:
        if s1 % 3 == s3 % 3 and s2 % 3 != a and s2 % 3 != b:
            # 跳过，这是余2，余1 ，余2结构
            vote_side = 0
            side = 1
        else:
            for index, aa in enumerate(list_1):
                if aa % 3 == a or aa % 3 == b:
                    list_f.append(aa)  # 获得余数与既定方案的数字
            if s1 < 14:  # 如果上一期为小,跟着买小，或者是反转
                if s2 > 13 and s3 < 14:
                    # 出现小大小结构，反转
                    shibie = 0
                    if temp_list:
                        for index, item in enumerate(temp_list[3:-2]):
                            if int(item) < 14:
                                # 假如这期为小，那我们要看下一期和下二期是否能够组成小大小结构。
                                if int(temp_list[index + 4]) > 13 and int(temp_list[index + 5]) < 14:
                                    if int(temp_list[index + 2]) > 13:
                                        shibie = shibie + 1 / (index + 1)
                                    elif int(temp_list[index + 2]) < 14:
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
            if s1 > 13:
                if s2 < 14 and s3 > 13:
                    # 大小大模式,反转，买中小
                    shibie = 0
                    if temp_list:
                        for index, item in enumerate(temp_list[3:-2]):
                            if int(item) > 13:
                                # 假如这期为大，那我们要看下一期和下二期是否能够组成大小大结构。
                                if int(temp_list[index + 4]) < 14 and int(temp_list[index + 5]) > 13:
                                    if int(temp_list[index + 2]) < 14:
                                        shibie = shibie + 1 / (index + 1)
                                    elif int(temp_list[index + 2]) > 13:
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
    else:
        vote_side = 0
        side = 0
    if vote_side == 0 and side == 0:
        print('上期为非投注类，直接跳过----,模式:', mmode)
        return []
    elif vote_side == 0 and side == 1:
        print('上期为010结构，直接跳过----,模式:', mmode)
        return []
    else:
        if vote_side == 1:
            for i in range(0, 14):
                if i in list_f:
                    list_num[i] = list_num[i] * bt * multiple
                else:
                    list_num[i] = 0
            for i in range(14, 28):
                list_num[i] = 0
            if side == 2:
                print(mmode, '正常投中小模式：', list_num, '投注倍率:', multiple)
            elif side == 3:
                print(mmode, '反转小模式：', list_num, '投注倍率:', multiple)
            return list_num
        elif vote_side == 2:
            for i in range(14, 28):
                if i in list_f:
                    list_num[i] = list_num[i] * bt * multiple
                else:
                    list_num[i] = 0
            for i in range(0, 14):
                list_num[i] = 0
            if side == 2:
                print(mmode, '正常投中大模式：', list_num, '投注倍率:', multiple)
            elif side == 3:
                print(mmode, '反转大模式：', list_num, '投注倍率:', multiple)
            return list_num


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


def vote_thing1(vote_current, list_v):  # 负责投注的函数
    return_list = []
    list_num = [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
    post_head = {"Accept": "text/html, application/xhtml+xml, */*",
                 "Accept-Encoding": "gzip, deflate",
                 "Accept-Language": "zh-cn",
                 "Cache-Control": "no-cache",
                 "Connection": "Keep-Alive",
                 "Content-Type": "application/x-www-form-urlencoded",
                 "Host": "www.lezhuan.com",
                 "Referer": "http://www.lezhuan.com/fun/insert.php?funNO=" + vote_current,
                 "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
                 "X-Requested-With": "XMLHttpRequest"}
    # 服务器接受str格式，把字典格式json格式转化
    a = {}
    for index, bb in enumerate(list_v):
        if bb > 0:
            a['tbChk[' + str((index + 3)) + ']'] = 'on'
    for index, bb in enumerate(list_v):
        if bb > 0:
            a['tbNum[' + str((index + 3)) + ']'] = bb
        else:
            a['tbNum[' + str((index + 3)) + ']'] = ''
    # c = json.dumps(a)
    # 毫秒级时间戳，同时作为postdata数据发现服务器
    # print(a)
    # print(gol_cookies)
    url = 'http://www.lezhuan.com/fun/insert.php?funNO=' + vote_current
    # Post数据服务器，cookies使用登录页面与验证码 合并cookies提交
    try:
        gol_cookies['cGlobal[last]'] = str(int(time.time()))
        req = requests.post(url, data=a, cookies=gol_cookies, headers=post_head,
                            allow_redirects=False, timeout=10)
        print('投注模块中，使用的全局cookies', gol_cookies)
        # print('打印投注返回信息:', req.content)
        if req.text.find('投注成功') > 0:
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


def vote_thing(vote_current, list_v):  # 负责投注的函数
    return_list = []
    list_num = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 63, 69, 73, 75, 75, 73, 69, 63, 55, 45, 36, 28, 21, 15, 10, 6, 3,
                1]
    get_head = {"Accept": "text/html, application/xhtml+xml, */*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-cn",
                "Connection": "Keep-Alive",
                "Host": "www.lezhuan.com",
                "Referer": "http://www.lezhuan.com/fast/",
                "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"
                }
    post_head = {"Accept": "text/html, application/xhtml+xml, */*",
                 "Accept-Encoding": "gzip, deflate",
                 "Accept-Language": "zh-cn",
                 "Cache-Control": "no-cache",
                 "Connection": "Keep-Alive",
                 "Content-Type": "application/x-www-form-urlencoded",
                 "Host": "www.lezhuan.com",
                 "Referer": "http://www.lezhuan.com/fast/insert.php?funNO=" + vote_current,
                 "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
                 "X-Requested-With": "XMLHttpRequest"}
    # 服务器接受str格式，把字典格式json格式转化

    # c = json.dumps(a)
    # 毫秒级时间戳，同时作为postdata数据发现服务器
    # print(a)
    # print(gol_cookies)
    url = 'http://www.lezhuan.com/fast/insert.php?fastNO=' + vote_current
    # Post数据服务器，cookies使用登录页面与验证码 合并cookies提交
    try:
        url_1 = "http://www.lezhuan.com/fast/insert.php?funNO=" + vote_current
        req_te = requests.get(url_1, cookies=gol_cookies, headers=get_head, allow_redirects=False, timeout=10)
        soup = BeautifulSoup(req_te.text, 'lxml')
        cc = soup.find('input', attrs={'type': "hidden", 'name': 'fast'})
        a = {}
        a['fast'] = cc['value']
        for index, bb in enumerate(list_v):
            if bb > 0:
                a['tbChk[' + str(index) + ']'] = 'on'
        for index, bb in enumerate(list_v):
            if bb > 0:
                a['tbNum[' + str(index) + ']'] = bb
            else:
                a['tbNum[' + str(index) + ']'] = ''
        gol_cookies['cGlobal[last]'] = str(int(time.time()))
        req = requests.post(url, data=a, cookies=gol_cookies, headers=post_head,
                            allow_redirects=False, timeout=10)
        print('投注模块中，使用的全局cookies', gol_cookies)
        print(a)
        # print('打印投注返回信息:', req.content)
        if req.text.find('投注成功') > 0:
            # f = open(fpath + '\\a.txt', 'a+')
            # f.write(vote_current.strip() + " 列表：" + str(list_v) + "\n")
            # f.close()
            for x in range(0, 28):
                if list_v[x] > list_num[x]:
                    return_list.append(x)
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
