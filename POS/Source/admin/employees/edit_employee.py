from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import mysql.connector
from API import administrative
from admin.pages import Pages

class EditEmployee(QMainWindow):
    def __init__(self,session,widget,cashierId):
        super().__init__()
        self.session = session
        self.widget = widget
        self.cashierId = cashierId
        loadUi("../UI/EditEmployee.ui",self)
        
        data = administrative.Employees.getCashierData(self.cashierId)

        #initial data
        self.firstnameForm.setText(data[0][0])
        self.middlenameForm.setText(data[0][1])
        self.lastnameForm.setText(data[0][2])
        self.usernameForm.setText(data[0][3])

        #Navigating buttons
        self.updateButton.clicked.connect(self.initiateUpdate)
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.inventoryButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))
        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.returnButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.logButton.clicked.connect(lambda: Pages.gotoLogs(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.promotionButton.clicked.connect(lambda: Pages.gotoPromotions(self.session,self.widget))

    
        #initialiazed
        self.errorMsg.setVisible(False)

    def initiateUpdate(self):
        
        try:
            administrative.Employees.updateCashier(self.cashierId,self.firstnameForm.text(),self.middlenameForm.text(),self.lastnameForm.text(),self.usernameForm.text(),self.passwordForm.text())
            Pages.gotoEmployees(self.session,self.widget)

        except mysql.connector.errors.IntegrityError:
            print("Failed")
            self.errorMsg.setVisible(True)
            self.errorMsg.setText("That username is taken!")
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))


