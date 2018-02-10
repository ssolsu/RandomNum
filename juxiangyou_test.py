import sys, time, os, Sqlite_16
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton)
import json, traceback
from PyQt5.QtCore import QThread


class Main_win(QWidget):
    def __init__(self):
        super(Main_win, self).__init__()
        self.initUI()
        self.t1 = Thread()
        self.t1.start()

    def initUI(self):
        self.setWindowTitle('juxiangyou Window')
        self.setGeometry(100, 100, 400, 400)
        self.sub_button = QPushButton('计算方法')
        self.layout = QVBoxLayout()
        self.ql = QLineEdit()
        self.setLayout(self.layout)
        # self.sub_button.clicked.connect(self.submit_site)
        self.layout.addWidget(self.ql)
        self.layout.addWidget(self.sub_button)
        self.t1 = Thread()
        # self.t1.start()


def vote_thing(vote_current, last_result, sp_flag, multiple):  # 负责投注的函数
    list_num = [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
    return_list = []
    if sp_flag == 0:  # 投注中单
        list_num[6] = list_num[6] * 10 * multiple
        list_num[8] = list_num[8] * 10 * multiple
        list_num[10] = list_num[10] * 10 * multiple
        list_num[last_result - 3] = list_num[last_result - 3] * 10 * multiple
        # print('投注买中单和上一期结果,倍数为:' + str(multiple))
        return_list = [9, 11, 13, last_result]
    else:  # 投注中双
        # print('投注买中单和上一期结果,倍数为:' + str(multiple))
        list_num[5] = list_num[5] * 10 * multiple
        list_num[7] = list_num[7] * 10 * multiple
        list_num[9] = list_num[9] * 10 * multiple
        list_num[last_result - 3] = list_num[last_result - 3] * 10 * multiple
        return_list = [8, 10, 12, last_result]
    print('经过修改后，投注的额度是列表是：', list_num, '倍率:', multiple)


class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()
        self.sq16 = Sqlite_16.Sqlite_db()
        # self.conn = self.sq16.get_conn()

    def run(self):
        try:
            sql = "select * from pc16 order by period asc  LIMIT 10 "
            result = self.sq16.fetch(sql)
            for x in result:
                print(x[0],'期数,开奖结果为',x[3])
            # print(result[10])
        except Exception as e:
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():%s' % traceback.format_exc())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = Main_win()
    mw.show()
    sys.exit(app.exec_())
