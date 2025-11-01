from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import mysql.connector
from API import administrative


class Pages:

    @staticmethod
    def gotoInventoryProduct(session,widget):
        panel = InventoryProduct(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    @staticmethod
    def gotoStatistics(session,widget):
        panel = Statistics(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    @staticmethod
    def gotoEmployees(session,widget):
        panel = Employees(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoAddEmployee(session,widget):
        panel = AddEmployee(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoEditEmployee(session,widget,cashierId):
        panel = EditEmployee(session,widget,cashierId)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Statistics(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()

        #session - Identify user and permission. widget passes widgets 
        self.session = session
        self.widget = widget
        loadUi("../UI/statistics.ui", self)

        topFive = administrative.Statistics.getTopFive()
    
        #Gives the sales data for sales overview.
        self.todayTotal.setText(str(administrative.Statistics.getTodayTotal()[0][0]))
        self.weeklyTotal.setText(str(administrative.Statistics.getWeeklyTotal()[0][0]))
        self.monthlyTotal.setText(str(administrative.Statistics.getMonthlyTotal()[0][0]))
        self.yearlyTotal.setText(str(administrative.Statistics.getYearlyTotal()[0][0]))
        
        #gets the top 5 sellers names.
        self.topOne.setText(topFive[0][0])
        self.topTwo.setText(topFive[1][0])
        self.topThree.setText(topFive[2][0])
        self.topFour.setText(topFive[3][0])
        self.topFive.setText(topFive[4][0])

        #gets the top 5 sellers total sold.
        self.countOne.setText(str(topFive[0][1]))
        self.countTwo.setText(str(topFive[1][1]))
        self.countThree.setText(str(topFive[2][1]))
        self.countFour.setText(str(topFive[3][1]))
        self.countFive.setText(str(topFive[4][1]))

        #Buttons that navigate to other pages.

        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.inventoryButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))
    
#--------------------------------------------------------------------------------------------------------------------------------

class Employees(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget
        loadUi("../UI/employees.ui",self)
        

        cashiers = administrative.Employees.getCashiers()

        #initialize employee table headers
        self.employeeTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.employeeTable.setColumnCount(5)
        self.employeeTable.setRowCount(len(cashiers))
        self.employeeTable.setColumnHidden(0, True)
        self.employeeTable.verticalHeader().setVisible(False)
        self.employeeTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.employeeTable.setHorizontalHeaderLabels(["userId","username","First Name", "Middle Name", "Last Name",])

        #double click event 
        self.employeeTable.cellDoubleClicked.connect(self.rowClickEvent)

        #Search event
        self.searchUsername.textChanged.connect(self.search)
        self.searchFirstname.textChanged.connect(self.search)
        self.searchMiddlename.textChanged.connect(self.search)
        self.searchLastname.textChanged.connect(self.search)

        

        tableRow = 0

        for row in cashiers:
            self.employeeTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.employeeTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.employeeTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.employeeTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.employeeTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(row[4])))

            tableRow += 1

        #Button change panels
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.addButton.clicked.connect(lambda: Pages.gotoAddEmployee(self.session,self.widget))

    def rowClickEvent(self,row,column):
        row_data = []
        
        for col in range(self.employeeTable.columnCount()):
            item = self.employeeTable.item(row, col)
            row_data.append(item.text() if item else "")

        Pages.gotoEditEmployee(self.session,self.widget,row_data[0])

    def search(self):
        data = administrative.Employees.searchParameters(self.searchUsername.text(),self.searchFirstname.text(),self.searchMiddlename.text(),self.searchLastname.text())
        
        tableRow = 0
        self.employeeTable.setRowCount(len(data))

        for row in data:
            self.employeeTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.employeeTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.employeeTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.employeeTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.employeeTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(row[4])))

            tableRow += 1

class AddEmployee(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget
        loadUi("../UI/AddEmployee.ui",self)

        
        self.errorMsg.setVisible(False)
        self.submit.clicked.connect(self.add)

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



#--------------------------------------------------------------------------------------------------------------------------------

class InventoryProduct(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget    
        self.productId = None

        loadUi("../UI/inventoryProduct.ui",self)

        products = administrative.Inventory.getProducts()

        #table info
        self.productTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.productTable.setColumnCount(4)
        self.productTable.setRowCount(len(products))
        self.productTable.setColumnHidden(0, True)
        self.productTable.verticalHeader().setVisible(False)
        self.productTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.productTable.setHorizontalHeaderLabels(["ProductID","Product Name","Price", "Total count"])

        #Set to invisible
        self.productName.setVisible(False)
        self.decrementButton.setVisible(False)
        self.incrementButton.setVisible(False)
        self.editPrice.setVisible(False)
        self.priceForm.setVisible(False)
        self.priceConfirm.setVisible(False)
        self.errorMsg.setVisible(False)

        #table events
        self.productTable.cellClicked.connect(self.singleClick)

        #button events
        self.priceConfirm.clicked.connect(self.updatePrice)
        self.decrementButton.clicked.connect(self.decrement)
        self.incrementButton.clicked.connect(self.increment)

        tableRow = 0

        for row in products:
            self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))

            tableRow += 1
    
    def decrement(self):
        try:
            administrative.Inventory.decrementCount(self.getProductId())
        except mysql.connector.errors.DatabaseError:
            self.errorMsg.setText("Stock cannot be less than 0!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))


        products = administrative.Inventory.getProducts()

        tableRow = 0

        for row in products:
            self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))

            tableRow += 1

    def increment(self):
        try:
            administrative.Inventory.incrementCount(self.getProductId())
        except mysql.connector.errors.DatabaseError:
            self.errorMsg.setText("Stock cannot be less than 0!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))


        products = administrative.Inventory.getProducts()

        tableRow = 0

        for row in products:
            self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))

            tableRow += 1


    def setProductId(self,productId):
        self.productId = productId

    def getProductId(self):
        return self.productId
    
    def updatePrice(self):
        try:
            administrative.Inventory.editPrice(self.priceForm.text(),self.getProductId())

            products = administrative.Inventory.getProducts()

            tableRow = 0

            for row in products:
                self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
                self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
                self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
                self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))

                tableRow += 1

        except mysql.connector.errors.DatabaseError:
            self.errorMsg.setText("Price cannot be less than or equal to 0!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))

    def singleClick(self,row,column):
        #fetch data here
        row_data = []
        
        for col in range(self.productTable.columnCount()):
            item = self.productTable.item(row, col)
            row_data.append(item.text() if item else "")

        self.setProductId(row_data[0])

        self.productName.setText(row_data[1])
        self.priceForm.setText(row_data[2])

        self.productName.setVisible(True)
        self.decrementButton.setVisible(True)
        self.incrementButton.setVisible(True)
        self.editPrice.setVisible(True)
        self.priceForm.setVisible(True)
        self.priceConfirm.setVisible(True)





