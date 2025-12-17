from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from API import administrative,cashier,general
from admin.logout import LogoutHandler
import os

class POS(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget 

        loadUi("../UI/cashier.ui",self)

        #instantiate POS object
        self.basket = cashier.POS()

        categories = administrative.Inventory.getCategories()
        self.categoryBox.currentIndexChanged.connect(self.onCategoryChange)
        self.searchForm.textChanged.connect(self.searchProduct)
        self.productTable.cellClicked.connect(self.imagePreview)
        self.productTable.cellDoubleClicked.connect(self.addToBasket)
        self.basketTable.cellClicked.connect(self.removeToBasket)
        self.checkoutButton.clicked.connect(self.checkout)
        self.logoutButton.clicked.connect(lambda: LogoutHandler.logout(self.widget))

        self.categoryBox.addItem("Any", None)

        for data in categories:
            self.categoryBox.addItem(data[1], data[0])
        
        products = cashier.Inventory.searchProduct(self.categoryBox.currentData(),self.searchForm.text())

        
        #invisible data
        self.subtotalLabel.setVisible(False)
        self.subtotal.setVisible(False)
        self.vatLabel.setVisible(False)
        self.totalVat.setVisible(False)
        self.errorMsg.setVisible(False)
        self.totalLabel.setVisible(False)
        self.total.setVisible(False)

        #table info
        self.productTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.productTable.setColumnCount(6)
        self.productTable.setRowCount(len(products))
        self.productTable.setColumnHidden(0, True)
        self.productTable.setColumnHidden(3, True)
        self.productTable.setColumnHidden(4, True)
        self.productTable.setColumnHidden(5, True)
        self.productTable.verticalHeader().setVisible(False)
        self.productTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.productTable.setHorizontalHeaderLabels(["ProductID","Product Name","Price","Icon ID", "Total count","Category"])   

        header = self.productTable.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        tableRow = 0

        for data in products:
            self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
            self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
            self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
            self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
            self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
            self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(None))
            tableRow += 1
        
        self.basketTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.basketTable.setColumnCount(4)
        self.basketTable.setColumnHidden(0, True)
        self.basketTable.setColumnHidden(3, True)
        self.basketTable.verticalHeader().setVisible(False)
        self.basketTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.basketTable.setHorizontalHeaderLabels(["Product ID","Product Name","Amount","Price"]) 

        header = self.basketTable.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def checkout(self):
        mode = self.checkoutButton.text()          

        if mode == "Checkout":
            if self.basket.getBasketSize() == 0:
                self.errorMsg.setText("Empty Basket!")
                self.errorMsg.setVisible(True)
                QTimer.singleShot(4000, lambda: self.errorMsg.setVisible(False))
                return

            if self.promoForm.text() == "":
                self.checkoutButton.setText("Confirm")
                QTimer.singleShot(5000, lambda: self.checkoutButton.setText("Checkout"))
            
            else:
                promoDetails = cashier.Promotions.usePromoCode(self.promoForm.text())
                print(promoDetails)

                if len(promoDetails) == 0:
                    self.errorMsg.setText("Invalid Coupon!")
                    self.subtotal.setText(str(self.basket.getSubtotal()))
                    self.totalVat.setText(str(self.basket.vatTotal()))
                    self.total.setText(str(self.basket.getTotal()))
                    self.errorMsg.setVisible(True)
                    QTimer.singleShot(4000, lambda: self.errorMsg.setVisible(False))

                    return

                else:
                    discountedSubTotal =  self.basket.useCoupon(float(promoDetails[0][3]) / 100)
                    discountedVat = self.basket.getDiscountedVat()
                    discountedTotal = self.basket.getDiscountedTotal()

                    self.subtotal.setText(str(discountedSubTotal))
                    self.totalVat.setText(str(discountedVat))
                    self.total.setText(str(discountedTotal))
                    
                    self.checkoutButton.setText("Confirm")
                    QTimer.singleShot(5000, lambda: self.checkoutButton.setText("Checkout"))
                    QTimer.singleShot(5000, lambda: self.subtotal.setText(str(self.basket.getSubtotal())))
                    QTimer.singleShot(5000, lambda: self.totalVat.setText(str(self.basket.vatTotal())))
                    QTimer.singleShot(5000, lambda: self.total.setText(str(self.basket.getTotal())))
                    
        elif mode == "Confirm":
            cash = self.cashForm.text()

            print()

            if self.promoForm.text() == "":
                try:
                    if float(cash) >= self.basket.getTotal():
                        change = float(cash) - self.basket.getTotal()

                        cashier.Invoice.issueInvoice(self.session["userID"],None,float(cash),change,self.basket.getTotal())

                        invoiceId = cashier.Invoice.getLastIssuedInvoice()[0][0]

                        for v in self.basket.getBasket().values():
                            cashier.Invoice.recordPurchases(v.getIdentifier(),invoiceId,v.getAmount())
                            cashier.Inventory.reduceStock(v.getIdentifier(),v.getAmount())

                        general.Invoice.generateReceipt(self.basket.getBasket(),self.basket.getSubtotal(),self.basket.vatTotal(),self.basket.getTotal(),self.session["userID"],float(cash),invoiceId)

                        self.basket.clearBasket()

                        self.basketTable.setRowCount(self.basket.getBasketSize())

                        tableRow = 0

                        for k,v in self.basket.getBasket().items():
                            self.basketTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(v.getIdentifier())))
                            self.basketTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(v.getProductName()))
                            self.basketTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(v.getAmount()))) 

                        products = cashier.Inventory.searchProduct(self.categoryBox.currentData(),self.searchForm.text())

                        if len(products) == 0:
                            return
        
                        if len(products[0]) == 5:
                            for data in products:
                                self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
                                self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
                                self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
                                self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
                                self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
                                self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(None))

                            tableRow += 1
                        
                        elif len(products[0]) == 6:
                            for data in products:
                                self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
                                self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
                                self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
                                self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
                                self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
                                self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(str(data[5])))

                                tableRow += 1
                        

                        self.cashForm.clear()
                        self.promoForm.clear()

                        self.subtotalLabel.setVisible(False)

                        self.subtotal.setVisible(False)
                        self.vatLabel.setVisible(False)
                        self.totalVat.setVisible(False)
                        self.errorMsg.setVisible(False)
                        self.totalLabel.setVisible(False)
                        self.total.setVisible(False)
                    
                        return

                    else:
                        self.errorMsg.setText("Insuffient Funds!")
                        self.errorMsg.setVisible(True)
                        QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
                except ValueError:
                    self.errorMsg.setText("Invalid Cash Input!")
                    self.errorMsg.setVisible(True)
                    QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
                    return
            else:
                promoDetails = cashier.Promotions.usePromoCode(self.promoForm.text())

                print(promoDetails)

                if len(promoDetails) == 0:
                    self.errorMsg.setText("Invalid Coupon!")
                    self.subtotal.setText(str(self.basket.getSubtotal()))
                    self.totalVat.setText(str(self.basket.vatTotal()))
                    self.total.setText(str(self.basket.getTotal()))
                    self.errorMsg.setVisible(True)
                    QTimer.singleShot(4000, lambda: self.errorMsg.setVisible(False))

                    return

                else:
                    discountedSubTotal =  self.basket.useCoupon(float(promoDetails[0][3]) / 100)
                    discountedVat = self.basket.getDiscountedVat()
                    discountedTotal = self.basket.getDiscountedTotal()

                    change = float(cash) - self.basket.getDiscountedTotal()

                    self.subtotal.setText(str(discountedSubTotal))
                    self.totalVat.setText(str(discountedVat))
                    self.total.setText(str(discountedTotal))

                    cashier.Invoice.issueInvoice(self.session["userID"],promoDetails[0][0],float(cash),change,self.basket.getDiscountedTotal())

                    invoiceId = cashier.Invoice.getLastIssuedInvoice()[0][0]

                    for v in self.basket.getBasket().values():
                        cashier.Invoice.recordPurchases(v.getIdentifier(),invoiceId,v.getAmount())
                        cashier.Inventory.reduceStock(v.getIdentifier(),v.getAmount())

                    general.Invoice.generateReceipt(self.basket.getBasket(),self.basket.useCoupon(float(promoDetails[0][3]) / 100),self.basket.getDiscountedVat(),self.basket.getDiscountedTotal(),self.session["userID"],float(cash),invoiceId)

                    self.basket.clearBasket()

                    self.basketTable.setRowCount(self.basket.getBasketSize())

                    tableRow = 0

                    for k,v in self.basket.getBasket().items():
                        self.basketTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(v.getIdentifier())))
                        self.basketTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(v.getProductName()))
                        self.basketTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(v.getAmount()))) 

                    products = cashier.Inventory.searchProduct(self.categoryBox.currentData(),self.searchForm.text())

                    if len(products) == 0:
                        return
        
                    if len(products[0]) == 5:
                        for data in products:
                            self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
                            self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
                            self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
                            self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
                            self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
                            self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(None))

                            tableRow += 1
                        
                    elif len(products[0]) == 6:
                        for data in products:
                            self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
                            self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
                            self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
                            self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
                            self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
                            self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(str(data[5])))

                            tableRow += 1
                    
                    self.cashForm.clear()
                    self.promoForm.clear()

                    self.subtotalLabel.setVisible(False)
                    self.subtotal.setVisible(False)
                    self.vatLabel.setVisible(False)
                    self.totalVat.setVisible(False)
                    self.errorMsg.setVisible(False)
                    self.totalLabel.setVisible(False)
                    self.total.setVisible(False)

                    return



            




    def removeToBasket(self,row,column):
        row_data = []

        

        for col in range(self.basketTable.columnCount()):
            item = self.basketTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        print(row_data)
        
        self.basket.getBasket()[int(row_data[0])].decrement()

        if self.basket.getBasket()[int(row_data[0])].getAmount() == 0:
            del self.basket.getBasket()[int(row_data[0])]

        self.basketTable.setRowCount(self.basket.getBasketSize())

        tableRow = 0

        for k,v in self.basket.getBasket().items():
            self.basketTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(v.getIdentifier())))
            self.basketTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(v.getProductName()))
            self.basketTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(v.getAmount())))     

            tableRow += 1
        
        if self.basket.getBasketSize() > 0:
            self.subtotal.setText(str(self.basket.getSubtotal()))
            self.totalVat.setText(str(self.basket.vatTotal()))
            self.total.setText(str(self.basket.getTotal()))
            self.subtotalLabel.setVisible(True)
            self.subtotal.setVisible(True)
            self.vatLabel.setVisible(True)
            self.totalVat.setVisible(True)
            self.totalLabel.setVisible(True)
            self.total.setVisible(True)
        else:
            self.subtotalLabel.setVisible(False)
            self.subtotal.setVisible(False)
            self.vatLabel.setVisible(False)
            self.totalVat.setVisible(False)
            self.totalLabel.setVisible(False)
            self.total.setVisible(False)


    def addToBasket(self,row,column):
        row_data = []
        
        for col in range(self.productTable.columnCount()):
            item = self.productTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        print(row_data)

        if int(row_data[4]) == 0:
            self.errorMsg.setText("Out of stock!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
            return

        punch = cashier.Product(row_data[0],row_data[1],row_data[2],row_data[4])

        if self.basket.addToBasket(punch) == "out of stock":
            self.errorMsg.setText("Out of stock!")
            self.errorMsg.setVisible(True)
            QTimer.singleShot(3000, lambda: self.errorMsg.setVisible(False))
            return

        self.basketTable.setRowCount(self.basket.getBasketSize())

        tableRow = 0

        for k,v in self.basket.getBasket().items():
            self.basketTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(v.getIdentifier())))
            self.basketTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(v.getProductName()))
            self.basketTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(v.getAmount())))   
            self.basketTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(v.getPrice())))    

            tableRow += 1
        
        self.basketTable.scrollToBottom()

        

        if self.basket.getBasketSize() > 0:
            self.subtotal.setText(str(self.basket.getSubtotal()))
            self.totalVat.setText(str(self.basket.vatTotal()))
            self.total.setText(str(self.basket.getTotal()))
            self.subtotalLabel.setVisible(True)
            self.subtotal.setVisible(True)
            self.vatLabel.setVisible(True)
            self.totalVat.setVisible(True)
            self.totalLabel.setVisible(True)
            self.total.setVisible(True)
        else:
            self.subtotalLabel.setVisible(False)
            self.subtotal.setVisible(False)
            self.vatLabel.setVisible(False)
            self.totalVat.setVisible(False)
            self.totalLabel.setVisible(False)
            self.total.setVisible(False)

        
        

        


    def imagePreview(self,row,column):
        row_data = []
        
        for col in range(self.productTable.columnCount()):
            item = self.productTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        icon = cashier.Inventory.getProductIcon(row_data[-3])[0][0]

        if os.path.exists(icon):
            pixmap = QPixmap(icon)
            self.iconPreview.setPixmap(pixmap)
        else:
            pixmap = QPixmap("icons/default.png")
            self.iconPreview.setPixmap(pixmap)
        

        



    def searchProduct(self):
        products = cashier.Inventory.searchProduct(self.categoryBox.currentData(),self.searchForm.text())
        print(products)

        self.productTable.setRowCount(len(products))

        tableRow = 0

        if len(products) == 0:
            return
        
        if len(products[0]) == 5:
            for data in products:
                self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
                self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
                self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
                self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
                self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
                self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(None))

                tableRow += 1
                        
        elif len(products[0]) == 6:
            for data in products:
                self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
                self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
                self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
                self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
                self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
                self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(str(data[5])))

                tableRow += 1

    def onCategoryChange(self):
        products = cashier.Inventory.searchProduct(self.categoryBox.currentData(),self.searchForm.text())
        
        self.productTable.setRowCount(len(products))

        tableRow = 0

        if len(products) == 0:
            return
        
        if len(products[0]) == 5:
            for data in products:
                self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
                self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
                self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
                self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
                self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
                self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(None))

                tableRow += 1
                        
        elif len(products[0]) == 6:
            for data in products:
                self.productTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(data[0])))
                self.productTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(data[1])))
                self.productTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(data[2])))
                self.productTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(data[3])))
                self.productTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(data[4])))
                self.productTable.setItem(tableRow,5,QtWidgets.QTableWidgetItem(str(data[5])))

                tableRow += 1
        
        