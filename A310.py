# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
import time,sys
from PyQt5.QtCore import QThread, pyqtSignal
import pymssql
import uuid
import _mssql
import decimal
print(decimal.__version__)
print(uuid.ctypes.__version__)
print(_mssql.__version__)


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
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 910, 43))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.label_1 = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label_1")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.label_1, 0, 3, 1, 1)
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
        self.tableWidget.setColumnCount(8)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "聚声泰系统物料查询"))
        self.groupBox.setTitle(_translate("MainWindow", "查询窗口"))
        self.label.setText(_translate("MainWindow", "查询："))
        self.label_1.setText(_translate("MainWindow", "(可以模糊查询料号或规格型号,如3.01.1001 或 Φ9.2)"))
        self.pushButton.setText(_translate("MainWindow", "查  询"))
        self.groupBox_2.setTitle(_translate("MainWindow", "剩余库存"))
        self.groupBox_3.setTitle(_translate("MainWindow", "物料反查/派单查询"))
        column_name = [
            '料号',
            '名称',
            '规格',
            '物料属性',
            '单位',
            '仓库',
            '批次',
            '数量',
        ]
        self.tableWidget.setHorizontalHeaderLabels(column_name)  # 设置列名称
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 170)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 60)
        self.tableWidget.setColumnWidth(5, 150)
        self.tableWidget.setColumnWidth(6, 150)
        self.tableWidget.setColumnWidth(6, 140)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 创建一条线程

    def update_item_data(self, data):
        yrow=self.tableWidget.rowCount()
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
        length = len(data)
        utf8_length = len(data.encode('utf-8'))
        length = (utf8_length - length) / 2 + length
        if length >= 2:
            server = '192.168.1.97'
            user = 'sa'
            password = 'xfcctv1983'
            result = []
            result1 = []
            yichun=[]
            conn = ''
            cur = ''
            try:
                conn = pymssql.connect(server, user, password, "AIS20180101102412")
                cur = conn.cursor()
                sql="SELECT a.FNumber,a.FName,a.FModel,a.FErpClsID,b.FName,a.FItemID FROM t_ICItem as a join t_MeasureUnit as b on a.FUnitID=b.FItemID  where a.FNumber like '%" + str(
                        data) + "%' or a.fmodel like '%" + str(data) + "%'"
                print(sql)
                cur.execute(sql)
                result = cur.fetchall()
                # cur.close()
                # print(result)
                if result:
                    for a in result:
                        cur = conn.cursor()
                        result1_sql = "SELECT a.FQty,b.fname,a.FBatchNo,a.fitemid FROM ICInventory as a join t_Stock as b on a.FStockID=b.fitemid where a.FQty<>0 AND a.FItemID='" + str(
                            a[5]) + "' UNION ALL SELECT a.FQty,b.fname,a.FBatchNo,a.fitemid FROM POInventory as a join t_Stock as b on a.FStockID=b.fitemid where a.fqty>0 and a.FItemID='" + str(
                            a[5]) + "'"
                        cur.execute(result1_sql)
                        result1 = cur.fetchall()
                        print(result1)
                        if result1:
                            for b in result1:
                                dqhs = self.tableWidget.rowCount()
                                self.tableWidget.insertRow(dqhs)
                                self.tableWidget.setItem(dqhs, 0, QtWidgets.QTableWidgetItem(str(a[0]).encode('latin1').decode('GBK')))
                                # 名称
                                self.tableWidget.setItem(dqhs, 1, QtWidgets.QTableWidgetItem(str(a[1]).encode('latin1').decode('GBK')))
                                # 规格
                                self.tableWidget.setItem(dqhs, 2, QtWidgets.QTableWidgetItem(str(a[2]).encode('latin1').decode('GBK')))
                                # 属性
                                if a[3] == 2:
                                    self.tableWidget.setItem(dqhs, 3, QtWidgets.QTableWidgetItem('自制'))
                                if a[3] == 1:
                                    self.tableWidget.setItem(dqhs, 3, QtWidgets.QTableWidgetItem('外购'))
                                # 单位
                                self.tableWidget.setItem(dqhs, 4, QtWidgets.QTableWidgetItem(str(a[4]).encode('latin1').decode('GBK')))
                                # 仓库
                                self.tableWidget.setItem(dqhs, 5, QtWidgets.QTableWidgetItem(str(b[1]).encode('latin1').decode('GBK')))
                                # 批次
                                self.tableWidget.setItem(dqhs, 6, QtWidgets.QTableWidgetItem(str(b[2]).encode('latin1').decode('GBK')))
                                # 数量
                                self.tableWidget.setItem(dqhs, 7, QtWidgets.QTableWidgetItem(str(round(b[0], 2)).encode('latin1').decode('GBK')))
                        else:
                            dqhs = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(dqhs)
                            self.tableWidget.setItem(dqhs, 0, QtWidgets.QTableWidgetItem(str(a[0]).encode('latin1').decode('GBK')))
                            # 名称
                            self.tableWidget.setItem(dqhs, 1, QtWidgets.QTableWidgetItem(str(a[1]).encode('latin1').decode('GBK')))
                            # 规格
                            self.tableWidget.setItem(dqhs, 2, QtWidgets.QTableWidgetItem(str(a[2]).encode('latin1').decode('GBK')))
                            # 属性
                            if a[3] == 2:
                                self.tableWidget.setItem(dqhs, 3, QtWidgets.QTableWidgetItem('自制'))
                            if a[3] == 1:
                                self.tableWidget.setItem(dqhs, 3, QtWidgets.QTableWidgetItem('外购'))
                            # 单位
                            self.tableWidget.setItem(dqhs, 4, QtWidgets.QTableWidgetItem(str(a[4]).encode('latin1').decode('GBK')))

                else:
                    QtWidgets.QMessageBox.information(self.centralwidget, "提示", "没有任何你所查询物料的信息",
                                                      QtWidgets.QMessageBox.Yes)
                    self.lineEdit.setFocus()
            except Exception as e:
                print(repr(e))
            finally:
                if conn != '':
                    conn.close()
            if cur != '':
                cur.close()
            conn.close()
        else:
            QtWidgets.QMessageBox.information(self.centralwidget, "提示", "你查询的内容少于3个中文或6个字母符号",
                                              QtWidgets.QMessageBox.Yes)
            self.lineEdit.setFocus()

    def update_table_row(self, data):
        self.tableWidget.setRowCount(data)

    def chaxun_clicked(self):
        self.t1 = UpdateTable()
        chaxun_content = self.lineEdit.text()
        self.t1.jieshou(chaxun_content)
        self.t1.update_date.connect(self.update_item_data)  # 链接信号
        self.t1.start()


class UpdateTable(QThread):
    """更新数据类"""

    update_date = pyqtSignal(str)
    update_1 = pyqtSignal(int)

    def jieshou(self, data):
        self.cx = data

    def run(self):
        print('线程中获取到的数据', self.cx)
        self.update_date.emit(self.cx)
        time.sleep(0.01)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())