import mysql.connector


connection = mysql.connector.connect(host="localhost",database="pos",user="root",password="root")
cursor = connection.cursor(prepared=True)

class Statistics:
    @staticmethod
    def getTodayTotal():
        query = """SELECT COALESCE(SUM(totalAmount), 0) AS total_amount_today FROM invoice WHERE DATE(timestampEvent) = CURDATE();"""
        cursor.execute(query,)
        result = cursor.fetchall()

        return result

    @staticmethod
    def getWeeklyTotal():
        query = """SELECT COALESCE(SUM(totalAmount), 0) AS total_amount_this_week FROM invoice WHERE YEARWEEK(timestampEvent, 1) = YEARWEEK(CURDATE(), 1);"""
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    @staticmethod
    def getMonthlyTotal():
        query = """SELECT COALESCE(SUM(totalAmount), 0) AS total_amount_this_month FROM invoice WHERE MONTH(timestampEvent) = MONTH(CURDATE()) AND YEAR(timestampEvent) = YEAR(CURDATE());"""
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    @staticmethod
    def getYearlyTotal():
        query = """SELECT COALESCE(SUM(totalAmount), 0) AS total_amount_this_year FROM invoice WHERE YEAR(timestampEvent) = YEAR(CURDATE());"""
        cursor.execute(query)
        result = cursor.fetchall()
    
        return result

    @staticmethod
    def topFive():
        query = """SELECT p.productId, p.productName, SUM(r.Quantity) AS total_quantity FROM records r JOIN products p ON r.productId = p.productId GROUP BY p.productId, p.productName ORDER BY total_quantity DESC LIMIT 5;"""
        cursor.execute(query)
        result = cursor.fetchall()

        return result