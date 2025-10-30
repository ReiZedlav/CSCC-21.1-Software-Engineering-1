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

        topFive = administrative.Statistics.getTopFive()
        print(topFive)

        #Gives the sales data for sales overview.
        self.todayTotal.setText(str(administrative.Statistics.getTodayTotal()[0][0]))
        self.weeklyTotal.setText(str(administrative.Statistics.getWeeklyTotal()[0][0]))
        self.monthlyTotal.setText(str(administrative.Statistics.getMonthlyTotal()[0][0]))
        self.yearlyTotal.setText(str(administrative.Statistics.getYearlyTotal()[0][0]))
        
        #gets the top 5 sellers names.
        self.topOne.setText(topFive[0][0])
        self.topTwo.setText(topFive[1][0])
        self.topThree.setText(topFive[2][0])
        self.topFour.setText(topFive[3][0])
        self.topFive.setText(topFive[4][0])

        #gets the top 5 sellers total sold.
        self.countOne.setText(str(topFive[0][1]))
        self.countTwo.setText(str(topFive[1][1]))
        self.countThree.setText(str(topFive[2][1]))
        self.countFour.setText(str(topFive[3][1]))
        self.countFive.setText(str(topFive[4][1]))