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
            return "out of stock"

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

        self.discountedSubtotal = 0
    
    def getBasket(self):
        return self.basket

    def getBasketSize(self):
        return len(self.basket)

    def addToBasket(self,product):
        if product.getIdentifier() in self.basket:
            if self.basket[product.getIdentifier()].increment() == "out of stock":
                return "out of stock"
            else:
                self.basket[product.getIdentifier()].increment()
        else:
            self.basket[product.getIdentifier()] = product
    
    def getTotal(self):
        return self.getSubtotal() + self.vatTotal()

    def vatTotal(self):
        vat = self.getSubtotal() * 0.12
        
        return vat

    def getSubtotal(self):
        self.total = 0
        for k,v in self.basket.items():
            self.total += v.getPrice() * v.getAmount()

        return self.total
    
#-------------------------------------------------------------------------------------

    def getDiscountedTotal(self):
        return self.discountedSubtotal + self.getDiscountedVat()

    def getDiscountedVat(self):
        vat = self.discountedSubtotal * 0.12

        return vat

    def useCoupon(self,rate):
        discount = self.getSubtotal() * rate

        self.discountedSubtotal = self.getSubtotal() - discount 

        return self.discountedSubtotal



class Promotions:
    @staticmethod
    def usePromoCode(code):
        query = """SELECT * FROM promotions WHERE promotionCode = %s;"""
        data = (code,)

        cursor.execute(query,data)

        result = cursor.fetchall()

        return result

class Inventory:
    @staticmethod
    def getProductIcon(iconid):
        query = """SELECT iconPath FROM icons WHERE iconId = %s"""

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

    
        
        