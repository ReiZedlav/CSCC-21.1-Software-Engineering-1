from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

from API import administrative

class Statistics(QMainWindow):
    def __init__(self,session):
        super().__init__()
        self.session = session
        loadUi("../UI/statistics.ui", self)
        #self.todayTotal.setText()

        self.todayTotal.setText(str(administrative.Statistics.getTodayTotal()[0][0]))
        self.weeklyTotal.setText(str(administrative.Statistics.getWeeklyTotal()[0][0]))
        self.monthlyTotal.setText(str(administrative.Statistics.getMonthlyTotal()[0][0]))
        self.yearlyTotal.setText(str(administrative.Statistics.getYearlyTotal()[0][0]))
        