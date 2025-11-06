import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

from API import general
from admin import adminPanel

#This is where it all begins.

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("../UI/login.ui", self)
        self.submitButton.clicked.connect(self.authenticate)

    def authenticate(self):
        username = self.usernameField.text()
        password = self.passwordField.text()

        cookies = general.Utils.login(username,password)

        print(cookies)

        
        #use try catch to prevent user enumeration when its bug free.
        if cookies["roleID"] == 1:
            panel = adminPanel.Statistics(cookies,widget)
            widget.addWidget(panel)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif cookies["roleID"] == 2:
            #goto cashier
            print("You are cashier!")
        





#GUI handler
app = QApplication(sys.argv)

mainwindow = Login()

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1200)
widget.setFixedHeight(800)
widget.show()

app.exec_()