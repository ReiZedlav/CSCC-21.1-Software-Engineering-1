from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from API import administrative
from admin.pages import Pages


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

        
        #initialize tables
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
        self.inventoryButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))
        self.addButton.clicked.connect(lambda: Pages.gotoAddEmployee(self.session,self.widget))
        self.logButton.clicked.connect(lambda: Pages.gotoLogs(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.promotionButton.clicked.connect(lambda: Pages.gotoPromotions(self.session,self.widget))


    #function for table click event
    def rowClickEvent(self,row,column):
        row_data = []
        
        for col in range(self.employeeTable.columnCount()):
            item = self.employeeTable.item(row, col)
            row_data.append(item.text() if item else "")

        Pages.gotoEditEmployee(self.session,self.widget,row_data[0])

    #self explanatory - searching lmaooooo
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

