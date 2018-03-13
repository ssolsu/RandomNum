from PyQt5.QtWidgets import QWidget, QTableWidget, QApplication, QPushButton, QVBoxLayout, QTableWidgetItem, \
    QAbstractItemView
import sys, time
from PyQt5.QtGui import QColor
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
            '状态',
            '连错',
            '买大小',
        ]
        self.talbe1.setHorizontalHeaderLabels(column_name)  # 设置列名称
        self.talbe1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.talbe1.setColumnWidth(0,100)
        self.talbe1.setColumnWidth(1, 100)
        self.talbe1.setColumnWidth(2, 100)
        self.talbe1.setColumnWidth(3, 100)
        self.talbe1.setColumnWidth(4, 50)
        self.talbe1.setColumnWidth(5, 50)
        self.talbe1.setColumnWidth(6, 50)
        self.talbe1.setColumnWidth(7, 50)
        self.talbe1.setColumnWidth(8, 50)
        self.talbe1.setColumnWidth(9, 50)
        self.talbe1.setColumnWidth(10, 50)
        self.talbe1.setColumnWidth(11, 50)
        self.talbe1.setColumnWidth(12, 50)
        self.talbe1.setColumnWidth(13, 50)
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
        wrong=0
        for i in range(0, rowcout - 20):
            maizhongflag = 0
            dxjg = ''
            vode_side = 0
            vode_dx = -1
            t_lst = []
            dqjg = int(self.talbe1.item(i, 3).text())
            xia1 = int(self.talbe1.item(i + 1, 3).text())
            xia2 = int(self.talbe1.item(i + 2, 3).text())
            xia3 = int(self.talbe1.item(i + 3, 3).text())
            xia4 = int(self.talbe1.item(i + 4, 3).text())
            xia5 = int(self.talbe1.item(i + 5, 3).text())
            if xia1 > 7 and xia1 < 20:
                vode_side = 1
                for w in range(1, 20):
                    t_lst.append(int(self.talbe1.item(i + w, 3).text()))
                print(t_lst)
                if (xia2 < 8 or xia2 > 19) and (xia3 > 7 and xia3 < 20):
                    vode_side = 0
                    for index, y in enumerate(t_lst[1:-10]):
                        if y > 7 and y < 20:
                            if (t_lst[index + 2] < 8 or t_lst[index + 2] > 19) and t_lst[index + 3] > 7 and t_lst[
                                        index + 3] < 20:
                                if t_lst[index] > 7 and t_lst[index] < 20:
                                    vode_side = 1
                                break
                elif (xia2 > 7 and xia2 < 20) and (xia3 < 8 or xia3 > 19):
                    for index, y in enumerate(t_lst[1:-10]):
                        if y > 7 and y < 20:
                            if (t_lst[index + 2] > 7 and t_lst[index + 2] < 20) and t_lst[index + 3] < 8 or t_lst[
                                        index + 3] > 19:
                                if t_lst[index] < 8 or t_lst[index] > 19:
                                    vode_side = 0
                                break
                elif (xia2 > 7 and xia2 < 20) and (xia3 > 7 and xia3 < 20) and (xia4 < 8 or xia4 > 19):
                    for index, y in enumerate(t_lst[1:-10]):
                        if y > 7 and y < 20:
                            if (t_lst[index + 2] > 7 and t_lst[index + 2] < 20) and (t_lst[index + 3] > 7 and t_lst[
                                    index + 3] < 20) and (t_lst[index + 4] < 8 or t_lst[
                                    index + 4] > 19):
                                if t_lst[index] < 8 or t_lst[index] > 19:
                                    vode_side = 0
                                break
                if xia1 < 14:
                    index=0
                    vode_dx = 0
                    if xia2 > 13:
                        for index, y in enumerate(t_lst[1:-3]):
                            if y < 14:
                                if (t_lst[index + 2] > 13):
                                    print(y, index, t_lst[index + 2],t_lst[index])
                                    if t_lst[index] > 13:
                                        vode_dx = 1
                                        print(self.talbe1.item(i,0).text(),t_lst,t_lst[index + 2],t_lst[index],index)
                                    break
                    elif xia2 < 14 and xia3 > 13:
                        for index, y in enumerate(t_lst[1:-3]):
                            if y < 14:
                                if (t_lst[index + 2] < 14 and t_lst[index + 3] > 13):
                                    if t_lst[index] > 13:
                                        vode_dx = 1
                                    break
                    # elif xia2 < 14 and xia3 < 14 and xia4 > 13:
                    #     for index, y in enumerate(t_lst[1:-4]):
                    #         if y < 14:
                    #             if (t_lst[index + 2] < 14 and t_lst[index + 3] < 14 and t_lst[index + 4] > 13):
                    #                 if t_lst[index] > 13:
                    #                     vode_dx = 1
                    #                     break
                else:
                    index=0
                    vode_dx = 1
                    if xia2 < 14:
                        for index, y in enumerate(t_lst[1:-3]):
                            if y > 13:
                                if (t_lst[index + 2] < 14):
                                    if t_lst[index] < 14:
                                        vode_dx = 0
                                    break
                    elif xia2 > 13 and xia3 < 14:
                        for index, y in enumerate(t_lst[1:-3]):
                            if y > 13:
                                if (t_lst[index + 2] > 13 and t_lst[index + 3] < 14):
                                    if t_lst[index] < 14:
                                        vode_dx = 0
                                    break
                    # elif xia2 > 13 and xia3 > 13 and xia4 < 14:
                    #     for index, y in enumerate(t_lst[1:-4]):
                    #         if y >13:
                    #             if (t_lst[index + 2] > 13 and t_lst[index + 3] > 13 and t_lst[index + 4] < 14):
                    #                 if t_lst[index] < 14:
                    #                     vode_dx = 0
                    #                     break
                if vode_side == 1 and vode_dx==0:
                    if (dqjg<14 and dqjg>7):
                        wrong=0
                        self.talbe1.setItem(i, 10, QTableWidgetItem('买小正确'))
                        self.talbe1.setItem(i,11,QTableWidgetItem(str(wrong)))
                    else:
                        wrong=wrong+1
                        self.talbe1.setItem(i, 10, QTableWidgetItem('买小错误'))
                        self.talbe1.setItem(i, 11, QTableWidgetItem(str(wrong)))

                elif vode_side==1 and vode_dx==1:
                    if (dqjg>13 and dqjg <20):
                        wrong=0
                        self.talbe1.setItem(i,10,QTableWidgetItem('买大正确'))
                        self.talbe1.setItem(i, 11, QTableWidgetItem(str(wrong)))
                    else:
                        wrong=wrong+1
                        self.talbe1.setItem(i, 10, QTableWidgetItem('买大错误'))
                        self.talbe1.setItem(i, 11, QTableWidgetItem(str(wrong)))


def maidaxiao(xia1, xia2, xia3, xia4, xia5, temp_list):
    maida = 0
    xia1 = int(xia1)
    xia2 = int(xia2)
    xia3 = int(xia3)
    xia4 = int(xia4)
    xia5 = int(xia5)
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
            # 独大模式要关注
            if xia2 < 14:
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
                maida = 1
        return maida


class thead(QThread):
    update_table = pyqtSignal(tuple)

    def run(self):
        conn = sqlite3.connect('shuju.db')
        cur = conn.cursor()
        # self.update_1.emit(rowcount[0])
        sql = "select * from jxy_fk28  where vote_time like '%03-11%' OR vote_time LIKE '%03-10%' ORDER by period DESC limit 1500"
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
