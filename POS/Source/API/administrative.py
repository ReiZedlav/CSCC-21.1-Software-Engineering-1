import mysql.connector
import bcrypt

connection = mysql.connector.connect(host="localhost",database="pos",user="root",password="")
cursor = connection.cursor(prepared=True)


class Promotions:
    @staticmethod
    def insertPromo(pname,pcode,pdiscount,pminimumpurchase):
        query = """INSERT INTO promotions(promotionName,promotionCode,discount,minimumPurchase) VALUES (%s,%s,%s,%s);"""
        data = (pname,pcode,pdiscount,pminimumpurchase)

        cursor.execute(query,data)

        connection.commit()

    @staticmethod 
    def getPromos():
        query = """SELECT * FROM promotions;"""

        cursor.execute(query,)

        result = cursor.fetchall()

        return result
    
    @staticmethod
    def updatePromo(promoId, pname,pcode,pdiscount,pminimumpurchase):
        query = """
        UPDATE promotions 
        SET promotionName = %s, promotionCode = %s, discount = %s, minimumPurchase = %s
        WHERE promotionId = %s
        """
        data = (pname,pcode,pdiscount,pminimumpurchase,promoId)
        cursor.execute(query,data)

        connection.commit()


    @staticmethod
    def removePromo(promoId):
        query = "DELETE FROM promotions WHERE promotionId = %s"
        values = (promoId,)
        cursor.execute(query, values)
        connection.commit()

class Logging:

    @staticmethod
    def getSpecificLogs(invoiceid,userid,product,timestamp):
        filteredInvoice = f"{invoiceid}%"
        filteredUserid = f"{userid}%"
        filteredProduct = f"{product}%"
        filteredTimestamp = f"{timestamp}%"
       
        data = (filteredInvoice,filteredUserid,filteredProduct,filteredTimestamp)

        query = """SELECT recordId,invoice.invoiceId,users.userId,productName,price,Quantity,timestampEvent,promotionName,totalCash,totalChange,totalAmount FROM records INNER JOIN invoice ON records.invoiceId = invoice.invoiceId INNER JOIN products ON records.productId = products.productId LEFT join promotions ON invoice.promotionId = promotions.promotionId INNER JOIN users ON users.userId = invoice.userId WHERE roleId = 2 AND invoice.invoiceId LIKE %s AND users.userId LIKE %s AND productName LIKE %s AND timestampEvent LIKE %s;"""

        cursor.execute(query,data)

        result = cursor.fetchall()

        return result


class Inventory:
    
    @staticmethod
    def addProductCategory(productid,categoryid):
        data = (productid,categoryid)

        query = """INSERT INTO productcategory(productId,categoryId) VALUES (%s,%s);"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod
    def removeProductCategory(productid,categoryid):
        data = (productid,categoryid)

        query = """DELETE FROM productcategory WHERE productId = %s and categoryId = %s;"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod
    def getSpecificCategoryListing(productid):
        data = (productid,)

        query = ("""SELECT categoryId, categoryName FROM category WHERE categoryId NOT IN (SELECT categoryId FROM productcategory WHERE productId = %s); """)
        
        cursor.execute(query,data)

        result = cursor.fetchall()

        return result

    @staticmethod
    def getSpecificProductCategory(productid):
        data = (productid,) 

        query = """SELECT category.categoryId,categoryName FROM productcategory LEFT JOIN category ON category.categoryId = productcategory.categoryId WHERE productId = %s; """

        cursor.execute(query,data)

        result = cursor.fetchall()

        return result

    @staticmethod
    def updateSpecificProduct(productname,price,stock,iconid,productid):
        data = (productname,price,iconid,stock,productid)

        query = """UPDATE products SET productName = %s, price = %s, iconId = %s, totalCount = %s WHERE productId = %s;"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod
    def getSpecificProduct(productId):
        data = (productId,)

        query = """SELECT productName,price,iconId,totalCount FROM products WHERE productId = %s;"""

        cursor.execute(query,data)

        result = cursor.fetchall()

        return result

    @staticmethod
    def setCategory(productId,categories):
        for i in categories:
            print(productId,i)
            data = (productId,i)

            query = """INSERT INTO productcategory(productId,categoryId) VALUES (%s,%s);"""

            cursor.execute(query,data)

            connection.commit()

    @staticmethod
    def getLastInsertedProductId():
        query = """SELECT LAST_INSERT_ID() FROM products LIMIT 1;"""

        cursor.execute(query,)

        result = cursor.fetchall()

        return result

    @staticmethod
    def addProduct(productName,price,iconId,totalCount):
        data = (productName,price,iconId,totalCount)

        query = """INSERT INTO products(productName,price,iconId,totalCount) VALUES (%s,%s,%s,%s);"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod
    def addCategory(categoryName):
        data = (categoryName,)

        query = """INSERT INTO category(categoryName) VALUES (%s);"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod
    def getCategories():
        query = """SELECT categoryId,categoryName FROM category;"""
        cursor.execute(query)

        result = cursor.fetchall()

        return result

    @staticmethod
    def editIcon(path,iconId):
        data = (path,iconId)

        query = """UPDATE icons SET iconPath = %s WHERE iconId = %s;"""

        cursor.execute(query,data)

        connection.commit()

    @staticmethod
    def addIcon(path):
        data = (path,)

        query = """INSERT into icons(iconPath) VALUES (%s);"""

        cursor.execute(query,data)

        connection.commit()

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
    def getFullname(userid):
        data = (userid,)

        query = """SELECT CONCAT(firstName,' ',middleName, ' ', lastName) AS FullName FROM users WHERE userId = %s;"""

        cursor.execute(query,data)

        result = cursor.fetchall()

        return result

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

        
    #dynamic UI employee search
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