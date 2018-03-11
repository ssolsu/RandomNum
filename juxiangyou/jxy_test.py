from PyQt5.QtWidgets import QWidget, QTableWidget, QApplication, QPushButton, QVBoxLayout, QTableWidgetItem, \
    QAbstractItemView
import sys, time
from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal
import sqlite3


class mywindow(QWidget):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui()

    def ui(self):
        self.setWindowTitle('测试程序')
        self.resize(1200, 700)
        self.yunsuan = QPushButton('开始运算')
        self.yunsuan.clicked.connect(self.update_js)
        vlayout = QVBoxLayout()
        self.talbe1 = QTableWidget()
        self.talbe1.setColumnCount(13)
        column_name = [
            '期数',
            '时间',
            '开奖号码',
            '开奖结果',
            '中',
            '边',
            '大',
            '小',
            '单',
            '双',
            '买中状态',
            '买中正确率',
            '买大小',
        ]
        self.talbe1.setHorizontalHeaderLabels(column_name)  # 设置列名称
        self.talbe1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        vlayout.addWidget(self.yunsuan)
        vlayout.addWidget(self.talbe1)
        self.setLayout(vlayout)
        self.t1 = thead()
        self.t1.update_table.connect(self.update_table)
        self.t1.start()

    def update_table(self, data):
        dqhs = self.talbe1.rowCount()
        self.talbe1.insertRow(dqhs)
        self.talbe1.setItem(dqhs, 0, QTableWidgetItem(data[0]))
        self.talbe1.setItem(dqhs, 1, QTableWidgetItem(data[1]))
        self.talbe1.setItem(dqhs, 2, QTableWidgetItem(data[2]))
        self.talbe1.setItem(dqhs, 3, QTableWidgetItem(data[3]))
        if int(data[3]) < 14:
            self.talbe1.setItem(dqhs, 7, QTableWidgetItem('小'))
        else:
            self.talbe1.setItem(dqhs, 6, QTableWidgetItem('大'))
        if int(data[3]) < 8 or int(data[3]) > 19:
            self.talbe1.setItem(dqhs, 5, QTableWidgetItem('边'))
        else:
            self.talbe1.setItem(dqhs, 4, QTableWidgetItem('中'))
        if int(data[3]) % 2 == 0:
            self.talbe1.setItem(dqhs, 9, QTableWidgetItem('双'))
        else:
            self.talbe1.setItem(dqhs, 8, QTableWidgetItem('单'))

    def update_js(self):
        t = Thread(target=self.update_js1)
        t.start()

    def update_js1(self):
        rowcout = self.talbe1.rowCount()
        flag = 0

        for i in range(0, rowcout):
            maizhongflag = 0
            dxjg=''
            temp_list = []
            dqjg = self.talbe1.item(i, 3).text()
            xia1 = self.talbe1.item(i + 1, 3).text()
            xia2 = self.talbe1.item(i + 2, 3).text()
            xia3 = self.talbe1.item(i + 3, 3).text()
            xia4 = self.talbe1.item(i + 4, 3).text()
            xia5 = self.talbe1.item(i + 5, 3).text()
            if int(xia1) > 7 and int(xia1) < 20:
                for w in range(1, 20):
                    temp_list.append(self.talbe1.item(i + w, 3).text())
                # print('说明下一期是中:')
                # 首先需要判断是不是中边中结构，如果是，搜索下面20期是否有中边中结构，如果有，假如是中，则购买，如果没有则跳过
                if (int(xia2) < 8 or int(xia2) > 19) and (int(xia3) > 7 and int(xia3) < 20):
                    print('满足当前是中边中结构')
                    for x in range(i + 3, i + 3 + 10):
                        if int(self.talbe1.item(x, 3).text()) > 7 and int(self.talbe1.item(x, 3).text()) < 20:
                            sou1 = int(self.talbe1.item(x + 1, 3).text())
                            sou2 = int(self.talbe1.item(x + 2, 3).text())
                            print('找到一个中，开始搜索中边中结构', sou1, sou2)
                            if (sou1 < 8 or sou1 > 19) and (sou2 > 7 and sou2 < 20):
                                print('获取到一个中边中结构，查询是否需要')
                                sou3 = int(self.talbe1.item(x - 1, 3).text())
                                # print('sou3', sou3)
                                if sou3 > 7 and sou3 < 20:
                                    maizhongflag = 1
                                    dxjg=maidaxiao(xia1,xia2,xia3,xia4,xia5,temp_list)
                                    self.talbe1.setItem(i, 10, QTableWidgetItem('买中'+str(dxjg)))
                                    print('这期要买中')
                                    break
                                else:
                                    print('这期要跳过')
                                    self.talbe1.setItem(i, 10, QTableWidgetItem('跳过'))
                                    break
                            else:
                                print('这期要跳过')
                                self.talbe1.setItem(i, 10, QTableWidgetItem('跳过'))
                else:
                    # 说明下一期是中，但不是中边中结构,第一，判断是否2连中，3连中，4连中结构
                    # 2连中结构
                    if int(xia2) > 7 and int(xia2) < 20 and (int(xia3) < 8 or int(xia3) > 19):
                        print('发现一个中中结构')
                        for x in range(i + 3, i + 3 + 10):
                            if int(self.talbe1.item(x, 3).text()) > 7 and int(self.talbe1.item(x, 3).text()) < 20:
                                sou1 = int(self.talbe1.item(x + 1, 3).text())
                                sou2 = int(self.talbe1.item(x + 2, 3).text())
                                print('找到一个中，开始搜索中中结构', sou1, sou2)
                                if sou1 > 7 and sou1 < 20:
                                    print('满足中中结构')
                                    if sou2 < 8 or sou2 > 19:
                                        self.talbe1.setItem(i, 10, QTableWidgetItem('中中跳过'))
                                    else:
                                        maizhongflag = 1
                                        dxjg = maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list)
                                        self.talbe1.setItem(i, 10, QTableWidgetItem('中中买中'+str(dxjg)))

                                        if int(dqjg) > 7 and int(dqjg) < 20:
                                            self.talbe1.setItem(i, 11, QTableWidgetItem('正确'))
                                        else:
                                            self.talbe1.setItem(i, 11, QTableWidgetItem('错误'))
                                    break
                                else:
                                    maizhongflag = 1
                                    dxjg = maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list)
                                    self.talbe1.setItem(i, 10, QTableWidgetItem('中中买中'+str(dxjg)))
                    # 3连结构
                    elif int(xia2) > 7 and int(xia2) < 20 and (int(xia3) > 7 and int(xia3) < 20) and (
                                    int(xia4) < 8 or int(xia4) > 19):
                        print('发现一个中中中结构')
                        for x in range(i + 3, i + 3 + 15):
                            if int(self.talbe1.item(x, 3).text()) > 7 and int(self.talbe1.item(x, 3).text()) < 20:
                                sou1 = int(self.talbe1.item(x + 1, 3).text())
                                sou2 = int(self.talbe1.item(x + 2, 3).text())
                                sou3 = int(self.talbe1.item(x + 3, 3).text())
                                print('找到一个中，开始搜索中中结构', sou1, sou2, sou3)
                                if sou1 > 7 and sou1 < 20 and sou2 > 7 and sou2 < 20:
                                    print('满足中中中结构')
                                    if sou3 < 8 or sou3 > 19:
                                        self.talbe1.setItem(i, 10, QTableWidgetItem('中中中跳过'))
                                    else:
                                        maizhongflag = 1
                                        dxjg = maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list)
                                        self.talbe1.setItem(i, 10, QTableWidgetItem('中中中买中'+str(dxjg)))
                                        if int(dqjg) > 7 and int(dqjg) < 20:
                                            self.talbe1.setItem(i, 11, QTableWidgetItem('正确'))
                                        else:
                                            self.talbe1.setItem(i, 11, QTableWidgetItem('错误'))
                                    break
                                else:
                                    maizhongflag = 1
                                    dxjg = maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list)
                                    self.talbe1.setItem(i, 10, QTableWidgetItem('中中中买中'+str(dxjg)))
                    # 4连中结构
                    elif int(xia2) > 7 and int(xia2) < 20 and (int(xia3) > 7 and int(xia3) < 20) and (
                                    int(xia4) > 7 and int(xia4) < 20) and (int(xia5) < 8 or int(xia5) > 19):
                        print('发现一个中中中中结构')
                        for x in range(i + 3, i + 3 + 15):
                            if int(self.talbe1.item(x, 3).text()) > 7 and int(self.talbe1.item(x, 3).text()) < 20:
                                sou1 = int(self.talbe1.item(x + 1, 3).text())
                                sou2 = int(self.talbe1.item(x + 2, 3).text())
                                sou3 = int(self.talbe1.item(x + 3, 3).text())
                                sou4 = int(self.talbe1.item(x + 4, 3).text())
                                print('找到一个中，开始搜索中中中中结构', sou1, sou2, sou3)
                                if sou1 > 7 and sou1 < 20 and sou2 > 7 and sou2 < 20 and sou3 > 7 and sou3 < 20:
                                    print('满足中中中中结构')
                                    if sou4 < 8 or sou4 > 19:
                                        self.talbe1.setItem(i, 10, QTableWidgetItem('中中中中跳过'))
                                    else:
                                        maizhongflag = 1
                                        dxjg = maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list)
                                        self.talbe1.setItem(i, 10, QTableWidgetItem('中中中中买中'+str(dxjg)))
                                        if int(dqjg) > 7 and int(dqjg) < 20:
                                            self.talbe1.setItem(i, 11, QTableWidgetItem('正确'))
                                        else:
                                            self.talbe1.setItem(i, 11, QTableWidgetItem('错误'))
                                    break
                                else:
                                    maizhongflag = 1
                                    dxjg = maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list)
                                    self.talbe1.setItem(i, 10, QTableWidgetItem('中中中中买中'+str(dxjg)))
                    else:
                        dxjg = maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list)
                        self.talbe1.setItem(i, 10, QTableWidgetItem('直接买中'+str(dxjg)))
                        maizhongflag = 1
                        if int(dqjg) > 7 and int(dqjg) < 20:
                            self.talbe1.setItem(i, 11, QTableWidgetItem('正确'))
                        else:
                            self.talbe1.setItem(i, 11, QTableWidgetItem('错误'))


def maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list):
    maida = 0
    xia1 = int(xia1)
    xia2 = int(xia2)
    xia3 = int(xia3)
    xia4 = int(xia4)
    xia5 = int(xia5)
    print(temp_list)
    # 下一期是大
    if xia1 > 13:
        # 判断是不是大小大，如果是
        if xia2 < 14 and xia3 > 13:
            # 大小大结构，找找之前的是否是
            for index, x in enumerate(temp_list[2:-5]):
                # 找到了一个大
                if int(x) > 13:
                    # 看下两期是小和大不
                    if int(temp_list[index + 3]) < 14 and int(temp_list[index + 4]) > 13:
                        # 找到了一个大小大，这时候，需要看看列表中上一期是什么
                        if int(temp_list[index + 1]) > 13:
                            maida = 1
                        break
        else:
            #独大模式要关注
            if xia2<14:
                for index, x in enumerate(temp_list[2:-5]):
                    # 找到了一个大
                    if int(x) > 13:
                        # 看下两一期是大不
                        if int(temp_list[index + 3]) > 13:
                            print('独大模式，直接买大')
                            maida = 1
                            break
            # 双大形态判断开始
            elif xia2 > 13 and xia3 < 14:
                # 找到独立双大
                for index, x in enumerate(temp_list[2:-5]):
                    # 找到了一个大
                    if int(x) > 13:
                        # 看下两一期是大不
                        if int(temp_list[index + 3]) > 13:
                            if int(temp_list[index + 4]) > 13:
                                print('连续大，直接买大')
                                maida = 1
                            break
            # 查找三连大
            elif xia2 > 13 and xia3 > 13 and xia4 < 14:
                # 找到独立三大
                for index, x in enumerate(temp_list[2:-5]):
                    # 找到了一个大
                    if int(x) > 13:
                        # 看下两一期是大不
                        if int(temp_list[index + 3]) > 13 and int(temp_list[index + 4]) > 13:
                            if int(temp_list[index + 5]) > 13:
                                print('连续大，直接买大')
                                maida = 1
                            break
            elif xia2 > 13 and xia3 > 13 and xia4 > 13 and xia5 < 14:
                # 找到独立四大
                for index, x in enumerate(temp_list[2:-5]):
                    # 找到了一个大
                    if int(x) > 13:
                        # 看下两一期是大不
                        if int(temp_list[index + 3]) > 13 and int(temp_list[index + 4]) > 13 and int(
                                temp_list[index + 5]) > 13:
                            if int(temp_list[index + 6]) > 13:
                                print('连续大，直接买大')
                                maida = 1
                            break
            else:
                maida=1
        return maida


class thead(QThread):
    update_table = pyqtSignal(tuple)

    def run(self):
        conn = sqlite3.connect('shuju.db')
        cur = conn.cursor()
        # self.update_1.emit(rowcount[0])
        sql = "select * from jxy_fk28  where vote_time like '%03-10%' OR vote_time LIKE '%03-09%' ORDER by period DESC limit 500"
        cur.execute(sql)
        result = cur.fetchall()
        for index, i in enumerate(result):
            row = (index,)
            data = i + row
            self.update_table.emit(data)
            time.sleep(0.01)


class thead1(QThread):
    jisuan_table = pyqtSignal(int)

    def lianjie(self):
        print('fuck')

    def run(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = mywindow()
    mw.show()
    sys.exit(app.exec_())
