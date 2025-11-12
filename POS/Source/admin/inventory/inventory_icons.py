from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from API import administrative, general
from admin.pages import Pages
import mysql.connector
import os
import re

class InventoryIcons(QMainWindow):
    def __init__(self,session,widget):
        super().__init__()
        self.session = session
        self.widget = widget  
        self.iconId = None
        loadUi("UI/inventoryIcons.ui",self)

        icons = administrative.Inventory.getIcons()

        #table info
        self.iconTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.iconTable.setColumnCount(3)
        self.iconTable.setRowCount(len(icons))
        self.iconTable.setColumnHidden(0, True)
        self.iconTable.verticalHeader().setVisible(False)
        self.iconTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.iconTable.setHorizontalHeaderLabels(["Icon ID","Icon Name","File Path"])

        header = self.iconTable.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        #table click events
        self.iconTable.cellClicked.connect(self.rowClick)

        #button click events
        self.addButton.clicked.connect(self.addIcon)
        self.overwriteButton.clicked.connect(self.overwriteIcon)
        self.returnButton.clicked.connect(lambda: Pages.gotoInventoryProduct(self.session,self.widget))

        

        #pixmap
        pixmap = QPixmap("icons/default.png")
        self.image.setPixmap(pixmap)
        
        #initialized
        self.errorMsg.setVisible(False)
        self.overwriteButton.setVisible(False)

        tableRow = 0


        for row in icons:
            self.iconTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.iconTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(self.getIconName(row[2])))
            
            self.iconTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            tableRow += 1

    # buttons change panels
        self.cashierButton.clicked.connect(lambda: Pages.gotoEmployees(self.session,self.widget))
        self.statButton.clicked.connect(lambda: Pages.gotoStatistics(self.session,self.widget))

    
    def overwriteIcon(self):
        dialog = QFileDialog()
        dialog.exec()

        selectedFile = dialog.selectedFiles()

        if selectedFile:
            file_name = selectedFile[0].split("/")[-1]
        
            file_extension = file_name.split('.')[-1].lower()

            accepted_extensions = ['png', 'jpeg', 'jpg', 'bmp', 'tiff', 'svg']
        
            if file_extension in accepted_extensions:
                resized_image = general.Icons.fitToPreview(selectedFile[0])

                resized_image.save(f"icons/{file_name}")

                administrative.Inventory.editIcon(f"icons/{file_name}",self.getIconId())

                pixmap = QPixmap(f"icons/{file_name}")
                self.errorMsg.setVisible(False)

                self.image.setPixmap(pixmap)

                icons = administrative.Inventory.getIcons()

                self.iconTable.setRowCount(len(icons))

                tableRow = 0

                for row in icons:
                    self.iconTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
                    self.iconTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(self.getIconName(row[2])))
                    self.iconTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
                    tableRow += 1

                print("success")
            else:
                self.errorMsg.setText("Invalid file format!")
                self.errorMsg.setVisible(True)
        

    def addIcon(self):
        dialog = QFileDialog()

        dialog.exec()

        selectedFile = dialog.selectedFiles()
        
        if selectedFile:
            file_name = selectedFile[0].split("/")[-1]
        
            file_extension = file_name.split('.')[-1].lower()

            accepted_extensions = ['png', 'jpeg', 'jpg', 'bmp', 'tiff', 'svg']
        
            if file_extension in accepted_extensions:
                resized_image = general.Icons.fitToPreview(selectedFile[0])

                resized_image.save(f"icons/{file_name}")

                try:
                    administrative.Inventory.addIcon(f"icons/{file_name}")
                except mysql.connector.errors.IntegrityError:
                    self.errorMsg.setText("That Image has already been used!")
                    self.errorMsg.setVisible(True)
                    
                    return 

                icons = administrative.Inventory.getIcons()

                self.iconTable.setRowCount(len(icons))

                tableRow = 0

                for row in icons:
                    self.iconTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(row[0])))
                    self.iconTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(self.getIconName(row[2])))
                    self.iconTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(row[2])))
                    tableRow += 1

                print("success")
            else:
                self.errorMsg.setText("Invalid file format!")
                self.errorMsg.setVisible(True)
    
    def getIconId(self):
        return self.iconId

    def setIconId(self,iconId):
        self.iconId = iconId

    def rowClick(self,row,column):
        row_data = []

        for col in range(self.iconTable.columnCount()):
            item = self.iconTable.item(row, col)
            row_data.append(item.text() if item else "")

        self.iconNamePreview.setText(self.getIconName(row_data[2]))
        
        print(row_data)

        self.setIconId(row_data[0])

        if os.path.exists(row_data[2]):
            print("Exist")
            pixmap = QPixmap(row_data[2])
            self.image.setPixmap(pixmap)
            self.errorMsg.setVisible(False)
            self.overwriteButton.setVisible(True)

        else:
            pixmap = QPixmap("icons/default.png")
            self.image.setPixmap(pixmap)
            self.errorMsg.setText("That file does not exist!")
            self.errorMsg.setVisible(True)
            self.overwriteButton.setVisible(True)
            
            



    def getIconName(self,iconName):
        png = iconName.split("/")[1]

        name = re.sub(r'\.png$', '', png)
        
        return name.capitalize()

