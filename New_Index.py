# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QHBoxLayout, QApplication,QGridLayout,QLineEdit,QPushButton,QMainWindow
from PyQt5.QtCore import QThread,pyqtSignal
import sys,sqlite3,time
import pymssql
import A310

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = A310.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
