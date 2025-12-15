import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow,QAbstractItemView
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from API import administrative
from admin.pages import Pages
from admin.logout import LogoutHandler

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
        self.promotionTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
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
        self.logoutButton.clicked.connect(lambda: LogoutHandler.logout(self.widget))
        
        #events
        self.promotionTable.cellClicked.connect(self.rowClick)
        self.addPromo.clicked.connect(self.newPromo)
        self.deletePromo.clicked.connect(self.delPromo)
        self.editPromo.clicked.connect(self.modifyPromo)

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

        self.refreshTable()
        self.clearForm()

    def delPromo(self):

        if not hasattr(self, 'selected_row_data'):
            self.errorMsg.setVisible(True)
            self.errorMsg.setText("Please select a promotion to delete!")
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
            return
    
        try:
            promotionId = self.selected_row_data[0]
            administrative.Promotions.removePromo(promotionId)
        except mysql.connector.errors.DatabaseError:
            self.errorMsg.setVisible(True)
            self.errorMsg.setText("Delete Failed!")
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
            return 

        self.refreshTable()
        self.clearForm()

    def modifyPromo(self):

        if not hasattr(self, 'selected_row_data'):
            self.errorMsg.setVisible(True)
            self.errorMsg.setText("Please select a promotion to edit")
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
            return

        try:   
            promotion_id = self.selected_row_data[0]
            administrative.Promotions.updatePromo(
                promotion_id,
                self.promotionNameForm.text(),
                self.promotionCodeForm.text(),
                self.discountForm.text(),
                self.minimumPurchaseForm.text()
            )

        except mysql.connector.errors.DatabaseError:
            self.errorMsg.setVisible(True)
            self.errorMsg.setText("Invalid Fields!")
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
            return 


        self.refreshTable()
        self.clearForm()
    
    def rowClick(self, row, column):
        self.selected_row_data = []
        self.selected_row_index = row 
    
        for col in range(self.promotionTable.columnCount()):
            item = self.promotionTable.item(row, col)
            self.selected_row_data.append(item.text() if item else "")
    
        self.promotionNameForm.setText(self.selected_row_data[1])  # Name
        self.promotionCodeForm.setText(self.selected_row_data[2])  # Code
        self.discountForm.setText(self.selected_row_data[3])       # Discount
        self.minimumPurchaseForm.setText(self.selected_row_data[4]) # Min Purchase
    
        print(f"Selected: {self.selected_row_data}")

    def refreshTable(self):
        promos = administrative.Promotions.getPromos()
        self.promotionTable.setRowCount(len(promos))
    
        tableRow = 0
        for row in promos:
            self.promotionTable.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.promotionTable.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.promotionTable.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.promotionTable.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.promotionTable.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            tableRow += 1

    def clearForm(self):
        self.promotionNameForm.clear()
        self.promotionCodeForm.clear() 
        self.discountForm.clear()
        self.minimumPurchaseForm.clear()
        # Clear the selection data
        if hasattr(self, 'selected_row_data'):
            del self.selected_row_data
        if hasattr(self, 'selected_row_index'):
            del self.selected_row_index
