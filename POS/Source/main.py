import sys
import cashierPanel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from API import general
from admin import statistics
from API import backupAutomate 

#This is where it all begins.

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("../UI/login.ui", self)
        self.setFixedWidth(569)
        self.setFixedHeight(299)
        self.setWindowTitle("Login")
       
        # Initialize backup
        self.backup_manager = backupAutomate.MySQLBackup()

        self.submitButton.clicked.connect(self.authenticate)


    def authenticate(self):
        username = self.usernameField.text()
        password = self.passwordField.text()

        cookies = general.Utils.login(username,password)

        print(cookies)

        
        #use try catch to prevent user enumeration when its bug free.

        if cookies is None:
            print("Login failed - invalid credentials")
            return
    
        if "roleID" not in cookies:
            print("Login failed - no roleID in response")
            return
        
        # ADD BACKUP ON LOGIN
        user_id = cookies.get("userID")
        role_id = cookies.get("roleID")
        
        print(f"User {user_id} logged in. Role: {role_id}. Creating backup...")
        
        # Run backup in background
        import threading
        def run_backup():
            success, message = self.backup_manager.create_backup()
            if success:
                print(f"Backup successful: {message}")
            else:
                print(f"Backup failed: {message}")
        
        # Start backup thread
        backup_thread = threading.Thread(target=run_backup)
        backup_thread.daemon = True
        backup_thread.start()
        
        if cookies["roleID"] == 1:
            panel = statistics.Statistics(cookies,widget)
            widget.addWidget(panel)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setWindowTitle("Admin - POS System")
            widget.setGeometry(10,30,1200,700)
            widget.setFixedWidth(1200)
            widget.setFixedHeight(700)

        elif cookies["roleID"] == 2:
            #goto cashier
            panel = cashierPanel.POS(cookies,widget)
            widget.addWidget(panel)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setWindowTitle("Cashier - POS System")
            widget.setGeometry(10,30,1200,700)
            widget.setFixedWidth(1200)
            widget.setFixedHeight(700)
            print("You are cashier!")
        





#GUI handler
app = QApplication(sys.argv)

mainwindow = Login()

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)

widget.setWindowTitle("POS System")
widget.show()

app.exec_()