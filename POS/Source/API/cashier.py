import mysql.connector

connection = mysql.connector.connect(host="localhost",database="pos",user="root",password="root")
cursor = connection.cursor(prepared=True)

class Product:
    def __init__(self,productid,productname,price,stock):
        self.productid = int(productid)
        self.productname = productname
        self.price = float(price)
        self.stock = int(stock)
        self.amount = 1
    
    def increment(self):
        if self.amount == self.stock:
            print("Out of stock")

        if self.amount < self.stock:
            self.amount += 1

    def getPrice(self):
        return self.price

    def decrement(self):
        self.amount -= 1

    def getIdentifier(self):
        return self.productid
    
    def getProductName(self):
        return self.productname
    
    def getAmount(self):
        return self.amount
    
    def toString(self):
        print(self.productid,self.productname,self.price,self.amount)

class POS:
    def __init__(self):
        self.basket = {}
        self.total = 0
    
    def getBasket(self):
        return self.basket

    def getBasketSize(self):
        return len(self.basket)

    def addToBasket(self,product):
        if product.getIdentifier() in self.basket:
            self.basket[product.getIdentifier()].increment()
        else:
            self.basket[product.getIdentifier()] = product
    
    def getTotal(self):
        self.total = 0
        for k,v in self.basket.items():
            self.total += v.getPrice() * v.getAmount()

        return self.total

    
class Inventory:
    @staticmethod
    def getProductIcon(iconid):
        query = """SELECT iconPath from icons WHERE iconId = %s"""

        data = (iconid,)

        cursor.execute(query,data)

        result = cursor.fetchall()

        return result

    @staticmethod
    def searchProduct(catId,searchString):
        
        searchFilter = f"{searchString}%"

        if catId == None:
            query = """SELECT * FROM products WHERE productName LIKE %s;"""
            
            data = (searchFilter,)

            cursor.execute(query,data)

            result = cursor.fetchall()

            return result

        else:
            query = """SELECT products.productId,productName,price,iconId,totalCount,categoryId FROM products INNER JOIN productcategory ON products.productId = productcategory.productId WHERE categoryId = %s and productName LIKE %s;"""
            
            data = (catId,searchFilter)

            cursor.execute(query,data)

            result = cursor.fetchall()

            return result

    
        
        