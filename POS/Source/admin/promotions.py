import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from API import administrative
from admin.pages import Pages

class Promotions(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget   
        
        loadUi("../UI/promotions.ui",self)
        promos = administrative.Promotions.getPromos()

        
        self.promotionTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.promotionTable.setColumnCount(5)
        self.promotionTable.setRowCount(len(promos))
        self.promotionTable.verticalHeader().setVisible(False)
        self.promotionTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.promotionTable.setHorizontalHeaderLabels(["Promotion ID","Promotion Name","Promotion Code","Discount %","Minimum Purchase"])
        self.promotionTable.setColumnHidden(0, True)

        header = self.promotionTable.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        self.errorMsg.setVisible(False)

        # Button change panels

        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.inventoryButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))
        self.logButton.clicked.connect(lambda: Pages.gotoLogs(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))
        self.promotionButton.clicked.connect(lambda: Pages.gotoPromotions(self.session,self.widget))

        #events
        self.promotionTable.cellClicked.connect(self.rowClick)
        self.addPromo.clicked.connect(self.newPromo)

        tableRow = 0

        for row in promos:
            self.promotionTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.promotionTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.promotionTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.promotionTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.promotionTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(row[4])))

            tableRow += 1

    def newPromo(self):
        
        try:
            administrative.Promotions.insertPromo(self.promotionNameForm.text(),self.promotionCodeForm.text(),self.discountForm.text(),self.minimumPurchaseForm.text())
        except mysql.connector.errors.DatabaseError:
            self.errorMsg.setVisible(True)
            self.errorMsg.setText("Invalid Fields!")
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
            return 

        promos = administrative.Promotions.getPromos()
        
        self.promotionTable.setRowCount(len(promos))

        tableRow = 0

        for row in promos:
            self.promotionTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.promotionTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.promotionTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.promotionTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.promotionTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(row[4])))

            tableRow += 1

        self.promotionNameForm.clear()
        self.promotionCodeForm.clear()
        self.discountForm.clear()
        self.minimumPurchaseForm.clear()

    def rowClick(self,row,column):
        row_data = []

        for col in range(self.promotionTable.columnCount()):
            item = self.promotionTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        print(row_data)
