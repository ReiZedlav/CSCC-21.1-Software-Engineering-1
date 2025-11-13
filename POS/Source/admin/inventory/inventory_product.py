from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import mysql.connector
from API import administrative
from admin.pages import Pages

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
        self.productTable.cellDoubleClicked.connect(self.doubleClick)


        #button events
        self.priceConfirm.clicked.connect(self.updatePrice)
        self.decrementButton.clicked.connect(self.decrement)
        self.incrementButton.clicked.connect(self.increment)

        #button event (navigator)
        self.iconButton.clicked.connect(lambda: Pages.gotoInventoryIcons(self.session,self.widget))
        self.addButton.clicked.connect(lambda: Pages.gotoInventoryAdd(self.session,self.widget))

        tableRow = 0

        for row in products:
            self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))

            tableRow += 1

        # Buttons change panels

        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.logButton.clicked.connect(lambda: Pages.gotoLogs(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.promotionButton.clicked.connect(lambda: Pages.gotoPromotions(self.session,self.widget))


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

    def doubleClick(self,row,column):
        row_data = []
        
        for col in range(self.productTable.columnCount()):
            item = self.productTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        print(row_data[0])
        
        Pages.gotoInventoryEdit(self.session,self.widget,row_data[0])

    def singleClick(self,row,column):
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
