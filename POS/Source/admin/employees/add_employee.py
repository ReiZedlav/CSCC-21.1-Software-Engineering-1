from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import mysql.connector
from API import administrative
from admin.pages import Pages

class AddEmployee(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget
        loadUi("../UI/AddEmployee.ui",self)

        
        self.errorMsg.setVisible(False)
        self.submit.clicked.connect(self.add)
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.inventoryButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))
        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.returnButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.logButton.clicked.connect(lambda: Pages.gotoLogs(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.promotionButton.clicked.connect(lambda: Pages.gotoPromotions(self.session,self.widget))

    def add(self):
        firstname = self.firstnameForm.text()
        middlename = self.middlenameForm.text()
        lastname = self.lastnameForm.text()
        username = self.usernameForm.text()
        password = self.passwordForm.text()

        if (not firstname.strip() or not middlename.strip() or not lastname.strip() or not username.strip() or not password.strip()):
            self.errorMsg.setText("Please fill all necessary information!")
            self.errorMsg.setVisible(True)

        else:
            try:
                administrative.Employees.addCashier(firstname,middlename,lastname,username,password)
                self.errorMsg.setText("Cashier added successfully!")
                self.errorMsg.setVisible(True)
                self.firstnameForm.clear()
                self.middlenameForm.clear()
                self.lastnameForm.clear()
                self.usernameForm.clear()
                self.passwordForm.clear()
            except mysql.connector.errors.IntegrityError:
                self.errorMsg.setText("That username is taken!")
                self.errorMsg.setVisible(True)
