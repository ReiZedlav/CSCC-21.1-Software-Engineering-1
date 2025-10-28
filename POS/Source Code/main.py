import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("../UI/login.ui", self)






#boilerplate 
app = QApplication(sys.argv)

mainwindow = Login()

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1000)
widget.setFixedHeight(600)
widget.show()

app.exec_()