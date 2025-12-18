from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from API import administrative
from admin.pages import Pages
from PyQt5.QtCore import QTimer
from admin.logout import LogoutHandler
import mysql.connector

class InventoryEdit(QMainWindow):
    def __init__(self,session,widget,productId):
        super().__init__()
        self.session = session
        self.widget = widget   
        self.productId = productId
        loadUi("../UI/inventoryEdit.ui",self)
        
        self.errorMsg.setVisible(False)

        categories = administrative.Inventory.getSpecificProductCategory(self.productId)

        categoryListing = administrative.Inventory.getSpecificCategoryListing(self.productId)

        for row in categoryListing:
            self.categoryBox.addItem(row[1], row[0])

        #table initialization
        self.categoryTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.categoryTable.setColumnCount(2)
        self.categoryTable.setRowCount(len(categories))
        self.categoryTable.setColumnHidden(0, True)
        self.categoryTable.verticalHeader().setVisible(False)
        self.categoryTable.setHorizontalHeaderLabels(["Category ID","Category"])

        header = self.categoryTable.horizontalHeader()
        header.setStretchLastSection(True)  

        #buttons
        self.overwriteButton.clicked.connect(self.updateProduct)        
        self.addCategory.clicked.connect(self.categorizeProduct)
        self.returnButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))
        self.logoutButton.clicked.connect(lambda: LogoutHandler.logout)
        self.newCategory_2.clicked.connect(self.newCategory)

        # buttons change panels
        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.logButton.clicked.connect(lambda: Pages.gotoLogs(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.promotionButton.clicked.connect(lambda: Pages.gotoPromotions(self.session,self.widget))


        #table click events
        self.categoryTable.cellDoubleClicked.connect(self.deleteRow)

        tableRow = 0

        for row in categories:
            self.categoryTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.categoryTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow += 1

        
        productInfo = administrative.Inventory.getSpecificProduct(self.productId)

        icons = administrative.Inventory.getIcons()

        for row in icons:
            self.iconBox.addItem(str(row[1].split("/")[1]), row[0])
            
        self.productnameForm.setText(str(productInfo[0][0]))
        self.priceForm.setText(str(productInfo[0][1]))
        self.stockForm.setText(str(productInfo[0][3]))

        default_icon = productInfo[0][2]

        for index, row in enumerate(icons):
            if row[0] == default_icon:
                self.iconBox.setCurrentIndex(index)
                break
        self.verifyAvailability()
    
    def verifyAvailability(self):
        if self.categoryBox.count() == 0:
            self.addCategory.setVisible(False)
            self.categoryBox.setVisible(False)
        else:
            self.addCategory.setVisible(True)
            self.categoryBox.setVisible(True)
    
    def categorizeProduct(self): 
        
    
        administrative.Inventory.addProductCategory(self.productId,self.categoryBox.currentData())

        categories = administrative.Inventory.getSpecificProductCategory(self.productId)
        categoryListing = administrative.Inventory.getSpecificCategoryListing(self.productId)

        self.categoryTable.setRowCount(len(categories))

        tableRow = 0

        for row in categories:
            self.categoryTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.categoryTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow += 1

        self.categoryBox.clear()

        for row in categoryListing:
            self.categoryBox.addItem(row[1], row[0])
        self.verifyAvailability()


    def deleteRow(self,row,column):
        row_data = []

        for col in range(self.categoryTable.columnCount()):
            item = self.categoryTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        administrative.Inventory.removeProductCategory(self.productId,row_data[0])

        categories = administrative.Inventory.getSpecificProductCategory(self.productId)

        self.categoryTable.setRowCount(len(categories))

        tableRow = 0

        for row in categories:
            self.categoryTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.categoryTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow += 1

        categoryListing = administrative.Inventory.getSpecificCategoryListing(self.productId)

        self.categoryBox.clear()

        for row in categoryListing:
            self.categoryBox.addItem(row[1], row[0])
        self.verifyAvailability()

    def newCategory(self):
        try:
            administrative.Inventory.addCategory(self.categoryForm.text())
            self.categoryForm.clear()
        except:
            self.errorMsg.setText("That category already exists!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))

        categories = administrative.Inventory.getSpecificProductCategory(self.productId)

        tableRow = 0

        for row in categories:
            self.categoryTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.categoryTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow += 1

        categoryListing = administrative.Inventory.getSpecificCategoryListing(self.productId)

        self.categoryBox.clear()

        for row in categoryListing:
            self.categoryBox.addItem(row[1], row[0])
        self.verifyAvailability()

    
        
    def updateProduct(self):
        productname = self.productnameForm.text()
        price = self.priceForm.text()
        stock = self.stockForm.text()
        iconid = self.iconBox.currentData()

        if (not productname.strip() or not price.strip() or not stock.strip()):
            self.errorMsg.setText("Forms cannot be blank!")
            self.errorMsg.setVisible(True)
        else:
            administrative.Inventory.updateSpecificProduct(productname,price,stock,iconid,self.productId)
            #edit category afterwards



            Pages.gotoInventoryProduct(self.session,self.widget)
        