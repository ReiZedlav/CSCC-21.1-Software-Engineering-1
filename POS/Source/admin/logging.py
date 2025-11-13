from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import mysql.connector
from API import administrative
from admin.pages import Pages

class Logging(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget   

        loadUi("../UI/logging.ui",self)

        logs = administrative.Logging.getSpecificLogs("","","","")

        #initialize log table
        self.logTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.logTable.setColumnCount(11)
        self.logTable.setRowCount(len(logs))
        self.logTable.verticalHeader().setVisible(False)
        self.logTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.logTable.setHorizontalHeaderLabels(["record ID","invoice ID","User ID", "Product", "Price","Quantity","Timestamp","Promotion","Total Cash","Total Change","Total Amount"])

        #Hide columns...
        self.logTable.setColumnHidden(0, True)
        self.logTable.setColumnHidden(7, True)
        self.logTable.setColumnHidden(8, True)
        self.logTable.setColumnHidden(9, True)
        self.logTable.setColumnHidden(10, True)

        #header
        header = self.logTable.horizontalHeader()
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)  

        #set Invis
        self.facilitatorLabel.setVisible(False)
        self.facilitatorOutput.setVisible(False)
        self.cashLabel.setVisible(False)
        self.cashOutput.setVisible(False)
        self.changeLabel.setVisible(False)
        self.changeOutput.setVisible(False)
        self.amountLabel.setVisible(False)
        self.amountOutput.setVisible(False)
        self.promoLabel.setVisible(False)
        self.promoOutput.setVisible(False)
       
        #button click events
        self.logTable.cellClicked.connect(self.rowClick)

        #text changes
        self.invoiceForm.textChanged.connect(self.logSearch)
        self.userForm.textChanged.connect(self.logSearch)
        self.productForm.textChanged.connect(self.logSearch)
        self.timestampForm.textChanged.connect(self.logSearch)

        #nav
        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.inventoryButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))
        self.logButton.clicked.connect(lambda: Pages.gotoLogs(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.promotionButton.clicked.connect(lambda: Pages.gotoPromotions(self.session,self.widget))


        tableRow = 0

        for row in logs:
            self.logTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.logTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.logTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.logTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.logTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(row[4])))
            self.logTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(str(row[5])))
            self.logTable.setItem(tableRow,6,QtWidgets.QTableWidgetItem(str(row[6])))
            self.logTable.setItem(tableRow,7,QtWidgets.QTableWidgetItem(str(row[7])))
            self.logTable.setItem(tableRow,8,QtWidgets.QTableWidgetItem(str(row[8])))
            self.logTable.setItem(tableRow,9,QtWidgets.QTableWidgetItem(str(row[9])))
            self.logTable.setItem(tableRow,10,QtWidgets.QTableWidgetItem(str(row[10])))

            tableRow += 1

    def logSearch(self):
        searched = administrative.Logging.getSpecificLogs(self.invoiceForm.text(),self.userForm.text(),self.productForm.text(),self.timestampForm.text())

        tableRow = 0

        self.logTable.setRowCount(len(searched))

        for row in searched:
            self.logTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.logTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.logTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.logTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.logTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(row[4])))
            self.logTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(str(row[5])))
            self.logTable.setItem(tableRow,6,QtWidgets.QTableWidgetItem(str(row[6])))
            self.logTable.setItem(tableRow,7,QtWidgets.QTableWidgetItem(str(row[7])))
            self.logTable.setItem(tableRow,8,QtWidgets.QTableWidgetItem(str(row[8])))
            self.logTable.setItem(tableRow,9,QtWidgets.QTableWidgetItem(str(row[9])))
            self.logTable.setItem(tableRow,10,QtWidgets.QTableWidgetItem(str(row[10])))
            
            tableRow += 1

    def rowClick(self,row,column):
        row_data = []

        for col in range(self.logTable.columnCount()):
            item = self.logTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        print(row_data)

        self.facilitatorOutput.setText(administrative.Employees.getFullname(row_data[2])[0][0])
        self.promoOutput.setText(row_data[-4])
        self.cashOutput.setText(row_data[-3])
        self.changeOutput.setText(row_data[-2])
        self.amountOutput.setText(row_data[-1])

        
        self.facilitatorLabel.setVisible(True)
        self.facilitatorOutput.setVisible(True)
        self.cashLabel.setVisible(True)
        self.cashOutput.setVisible(True)
        self.changeLabel.setVisible(True)
        self.changeOutput.setVisible(True)
        self.amountLabel.setVisible(True)
        self.amountOutput.setVisible(True)
        self.promoLabel.setVisible(True)
        self.promoOutput.setVisible(True)