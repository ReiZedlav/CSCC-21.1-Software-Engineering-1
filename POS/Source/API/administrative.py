import mysql.connector
import bcrypt

connection = mysql.connector.connect(host="localhost",database="pos",user="root",password="root")
cursor = connection.cursor(prepared=True)

class Inventory:

    @staticmethod
    def getIcons():
        query = """SELECT iconId,iconPath,iconPath from icons;"""

        cursor.execute(query,)

        result = cursor.fetchall()

        return result

    @staticmethod
    def decrementCount(productId):
        data = (productId,)

        query = """UPDATE products set totalCount = totalCount - 1 WHERE productId = %s;"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod
    def incrementCount(productId):
        data = (productId,)

        query = """UPDATE products set totalCount = totalCount + 1 WHERE productId = %s;"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod
    def editPrice(newPrice,productId):
        data = (newPrice,productId)

        query = """UPDATE products SET price = %s WHERE productId = %s;"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod 
    def getProducts():
        query = """SELECT productId,productName,price,totalCount from products;"""

        cursor.execute(query,)

        result = cursor.fetchall()

        return result
    


class Employees:

    @staticmethod
    def updateCashier(cashierId,firstname,middlename,lastname,username,password):
        if not password.strip():
            data = (firstname,middlename,lastname,username,cashierId)

            query = """UPDATE users set firstName = %s, middleName = %s, lastName = %s, username = %s WHERE userId = %s;"""

            cursor.execute(query,data)

            connection.commit()

        else:
            hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            hashed_str = hashed_bytes.decode("utf-8")

            data = (firstname,middlename,lastname,username,hashed_str,cashierId)

            query = """UPDATE users SET firstName = %s, middleName = %s, lastName = %s, username = %s, HashedPassword = %s WHERE userId = %s;"""

            cursor.execute(query,data)

            connection.commit()
        

    @staticmethod
    def getCashierData(cashierId):
        data = (cashierId,)

        query = """SELECT firstName,middleName,lastName,userName FROM users WHERE userId = %s;"""

        cursor.execute(query,data)

        result = cursor.fetchall()

        return result

    @staticmethod
    def addCashier(firstname,middlename,lastname,username,password):
        print(firstname,middlename,lastname,username,password)
        #turn password to bcrypt here
        hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        hashed_str = hashed_bytes.decode("utf-8")

        data = (firstname,middlename,lastname,username,hashed_str,2)

        query = """INSERT INTO users(firstName,middlename,lastname,username,HashedPassword,roleId) VALUES (%s,%s,%s,%s,%s,%s);"""

        cursor.execute(query,data)

        connection.commit()

        

    @staticmethod
    def searchParameters(username,firstname,middlename,lastname):
        userNameFilter = f"{username}%"
        firstNameFilter = f"{firstname}%"
        middleNameFilter = f"{middlename}%"
        lastNameFilter = f"{lastname}%"

        data = (userNameFilter,firstNameFilter,middleNameFilter,lastNameFilter)

        query = """SELECT userId,userName,firstName,middleName,lastName FROM users where roleId = 2 AND userName LIKE %s AND firstName LIKE %s AND middleName LIKE %s AND lastName LIKE %s;"""

        cursor.execute(query,data)
        result = cursor.fetchall()

        return result

    @staticmethod
    def getCashiers():
        query = """SELECT userId,userName,firstName,middleName,lastName FROM users WHERE roleId = 2;"""
        cursor.execute(query,)
        result = cursor.fetchall()

        return result






class Statistics:
    #gets the total revenue for today.
    @staticmethod
    def getTodayTotal():
        query = """SELECT COALESCE(SUM(totalAmount), 0) AS total_amount_today FROM invoice WHERE DATE(timestampEvent) = CURDATE();"""
        cursor.execute(query,)
        result = cursor.fetchall()

        return result

    #gets the total revenue for the week
    @staticmethod
    def getWeeklyTotal():
        query = """SELECT COALESCE(SUM(totalAmount), 0) AS total_amount_this_week FROM invoice WHERE YEARWEEK(timestampEvent, 1) = YEARWEEK(CURDATE(), 1);"""
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    #gets total revenue for the month
    @staticmethod
    def getMonthlyTotal():
        query = """SELECT COALESCE(SUM(totalAmount), 0) AS total_amount_this_month FROM invoice WHERE MONTH(timestampEvent) = MONTH(CURDATE()) AND YEAR(timestampEvent) = YEAR(CURDATE());"""
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    #gets total revenue for the year
    @staticmethod
    def getYearlyTotal():
        query = """SELECT COALESCE(SUM(totalAmount), 0) AS total_amount_this_year FROM invoice WHERE YEAR(timestampEvent) = YEAR(CURDATE());"""
        cursor.execute(query)
        result = cursor.fetchall()
    
        return result

    #gets the top 5 most popular items in terms of purchased 
    @staticmethod
    def getTopFive():
        query = """SELECT p.productName, SUM(r.Quantity) AS total_quantity FROM records r JOIN products p ON r.productId = p.productId GROUP BY p.productId, p.productName ORDER BY total_quantity DESC LIMIT 5;"""
        cursor.execute(query)
        result = cursor.fetchall()

        return result