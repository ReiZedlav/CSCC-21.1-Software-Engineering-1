from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import mysql.connector
from API import administrative
from admin.pages import Pages
from admin.logout import LogoutHandler

class InventoryAdd(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget   

        loadUi("../UI/inventoryAdd.ui",self)

        self.selected = []

        categories = administrative.Inventory.getCategories()

        #table initialization
        self.categoryTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.categoryTable.setColumnCount(2)
        self.categoryTable.setRowCount(len(categories))
        self.categoryTable.setColumnHidden(0, True)
        self.categoryTable.verticalHeader().setVisible(False)
        self.categoryTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.categoryTable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.categoryTable.setHorizontalHeaderLabels(["Category ID","Category"])

        self.errorMsg.setVisible(False)
        
        #button events
        self.categoryAdd.clicked.connect(self.addCategory)
        self.productSubmit.clicked.connect(self.submitProduct)
        self.returnButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))


        #table events
        self.categoryTable.cellClicked.connect(self.rowClick)
        

        header = self.categoryTable.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        tableRow = 0

        

        for row in categories:
            self.categoryTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.categoryTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow += 1

        icons = administrative.Inventory.getIcons()

        for row in icons:
            self.iconBox.addItem(str(row[1].split("/")[1]), row[0])

        # buttons change panels
        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.logButton.clicked.connect(lambda: Pages.gotoLogs(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.promotionButton.clicked.connect(lambda: Pages.gotoPromotions(self.session,self.widget))
        self.logoutButton.clicked.connect(lambda: LogoutHandler.logout(self.widget))
    
    def submitProduct(self):
        name = self.productnameForm.text()
        price = self.priceForm.text()
        stock = self.stockForm.text()
        iconId = self.iconBox.currentData()
        if (not name.strip() or not price.strip() or not stock.strip()):
            self.errorMsg.setText("Please fill all necessary information!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))

        else:
            try:
                administrative.Inventory.addProduct(name,price,stock,iconId)
            except mysql.connector.errors.DatabaseError:
                self.errorMsg.setText("Price cannot be 0 or Stock cannot be less than 0")
                self.errorMsg.setVisible(True)
                QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))

                return 

            productId = administrative.Inventory.getLastInsertedProductId()[0][0]

            administrative.Inventory.setCategory(productId,self.getSelected())
        

    def getSelected(self):
        return self.selected

    def addCategory(self):
        if self.categoryForm.text().strip() == "":
            self.errorMsg.setText("Category cannot be blank!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
            return 
            
        try:
            administrative.Inventory.addCategory(self.categoryForm.text())
        except:
            self.errorMsg.setText("That category already exists!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))

            return 

        categories = administrative.Inventory.getCategories()
        self.categoryTable.setRowCount(len(categories))

        tableRow = 0

        for row in categories:
            self.categoryTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.categoryTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow += 1
        self.categoryForm.clear()

    def rowClick(self,row,column):
        row_data = []

        for col in range(self.categoryTable.columnCount()):
            item = self.categoryTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        if row_data[0] in self.selected:
            self.selected.remove(row_data[0])
        else:
            self.selected.append(row_data[0])

        print(self.selected)

