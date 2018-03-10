# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '0310-1118.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3, time
from PyQt5.QtCore import QThread, pyqtSignal
import pymssql
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1073, 586)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 1051, 81))
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet("border-color: rgb(255, 32, 32);")
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 258, 43))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.chaxun_clicked)
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 260, 1051, 261))
        self.groupBox_2.setAutoFillBackground(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 1031, 231))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 100, 1051, 151))
        self.groupBox_3.setObjectName("groupBox_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 773, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "查询窗口"))
        self.label.setText(_translate("MainWindow", "查询："))
        self.pushButton.setText(_translate("MainWindow", "查  询"))
        self.groupBox_2.setTitle(_translate("MainWindow", "剩余库存"))
        self.groupBox_3.setTitle(_translate("MainWindow", "物料应用"))
        column_name = [
            '料号',
            '名称',
            '规格',
            '物料属性',
            '单位',
            '仓库',
            '数量',
        ]
        self.tableWidget.setHorizontalHeaderLabels(column_name)  # 设置列名称
        # 创建一条线程

    def update_item_data(self, data):
        server = '192.168.1.97'
        user = 'sa'
        password = 'xfcctv1983'
        result = []
        try:
            conn = pymssql.connect(server, user, password, "AIS20180226172529", charset='GBK')
            cur = conn.cursor()
            cur.execute(
                "SELECT a.FNumber,a.FName,a.FModel,a.FErpClsID,b.FName FROM t_ICItem as a join t_MeasureUnit as b on a.FUnitID=b.FItemID  where a.FNumber='" + str(
                    data) + "'")
            result = cur.fetchall()
            print(result)
        except Exception as e:
            print(repr(e))
        finally:
            conn.close()
        conn.close()
        if len(result[0]) > 4:
            self.tableWidget.setColumnWidth(0,100)
            self.tableWidget.setColumnWidth(1, 100)
            self.tableWidget.setColumnWidth(2, 100)
            self.tableWidget.setColumnWidth(3, 100)
            self.tableWidget.setColumnWidth(4, 100)
            self.tableWidget.setColumnWidth(5, 100)
            self.tableWidget.setColumnWidth(6, 100)
            self.tableWidget.setColumnWidth(7, 100)
            dqhs = self.tableWidget.rowCount()
            self.tableWidget.insertRow(dqhs)
            self.tableWidget.setItem(dqhs, 0, QtWidgets.QTableWidgetItem(result[0][0]))

            self.tableWidget.setItem(dqhs, 1, QtWidgets.QTableWidgetItem(result[0][1]))
            self.tableWidget.setItem(dqhs, 2, QtWidgets.QTableWidgetItem(result[0][2]))
            if result[0][3] == 2:
                self.tableWidget.setItem(dqhs, 3, QtWidgets.QTableWidgetItem('自制'))
            if result[0][3] == 1:
                self.tableWidget.setItem(dqhs, 3, QtWidgets.QTableWidgetItem('外购'))
            self.tableWidget.setItem(dqhs, 4, QtWidgets.QTableWidgetItem(result[0][4]))

    def update_table_row(self, data):
        self.tableWidget.setRowCount(data)

    def chaxun_clicked(self):
        self.t1 = UpdateTable()
        # bb = pyqtSignal(str)
        # print('啊啊啊啊啊')
        chaxun_content = self.lineEdit.text()
        # bb.emit(chaxun_content)
        self.t1.jieshou(chaxun_content)
        self.t1.update_date.connect(self.update_item_data)  # 链接信号
        self.t1.update_1.connect(self.update_table_row)
        self.t1.start()


class UpdateTable(QThread):
    """更新数据类"""

    update_date = pyqtSignal(str)  # pyqt5 支持python3的str，没有Qstring
    update_1 = pyqtSignal(int)

    def jieshou(self, data):
        self.cx = data

    def run(self):
        print('线程中获取到的数据', self.cx)
        # global chaxun_data
        # print('run线程中运行的chaxun_data数据',chaxun_data)
        self.update_date.emit(self.cx)
        time.sleep(0.01)
