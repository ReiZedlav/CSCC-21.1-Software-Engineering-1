from PIL import Image
import mysql.connector
import bcrypt
import calendar
import datetime
import os

#everything thats not administrative or used by cashier belongs here.

connection = mysql.connector.connect(host="localhost",database="pos",user="root",password="root")
cursor = connection.cursor(prepared=True)

class Invoice:
    @staticmethod
    def generateReceipt(basket,subtotal,vat,total,cashierid,cash,invoiceid):
        ct = datetime.datetime.now()
        filename = str(int(ct.timestamp()))
        
        date = ct.strftime("%Y-%m-%d")

        receipt = f"""
        D-TWO HARDWARE STORE
        XAVIER UNIVERSITY - ATENEO DE CAGAYAN
        CAGAYAN DE ORO CITY
        __________________________________________

        Invoice ID: {invoiceid}

        Transaction Handled by cashier: {cashierid}
        
        Transaction Occured On: {date}
        __________________________________________

        ------------------------------------------
        SALES INVOICE
        ------------------------------------------
        """

        receipt += "\n"

        for k in basket.values():
            receipt += "        " + str(k.getAmount()) + " " + k.getProductName() + " - " + str(k.getPrice() * k.getAmount()) 
            receipt += "\n"
        
        receipt += "        " + "__________________________________________"
        receipt += "\n"
        receipt += "\n"
        receipt += "        " + "Cash: " + str(cash)
        receipt += "\n"
        receipt += "        " + "Subtotal: " + str(subtotal)
        receipt += "\n"
        receipt += "        " + "VAT (12%): " + str(vat)
        receipt += "\n"
        receipt += "        " + "Total: " + str(total)
        receipt += "\n"
        receipt += "        " + "__________________________________________"
        receipt += "\n"
        receipt += "\n"
        receipt += "        " + "Thank you for shoping with us! Please come again!"

        print(receipt)
        with open(f"../../Receipts/{filename}.txt", "w") as file:
            file.write(receipt)

        
            
            


class Icons:
    @staticmethod 
    def fitToPreview(inputFile):
        
        image = Image.open(inputFile)

        w = 250
        h = 250

        resized = image.resize((w,h),Image.Resampling.LANCZOS)

        return resized

class Utils():
    @staticmethod
    def login(username,password):
        data = (username,)
        query = """SELECT userId,roleId,HashedPassword FROM Users WHERE username = %s"""
        
        cursor.execute(query,data)
        result = cursor.fetchall()

        print(result)

        #keep track of user, and authorization. 
        cookies = {
            "userID": None,
            "roleID": None
        }

        try:
            cookies["userID"] = result[0][0]
            cookies["roleID"] = result[0][1]
            bcryptPassword = result[0][2]
        except IndexError:
            print(cookies)
            return None
        try:
            verified = bcrypt.checkpw(password.encode('utf-8'),bcryptPassword.encode('utf-8'))
            
            if verified:

                return cookies

            else:
                print(cookies)
                return None
            
        except UnboundLocalError:
            print(cookies)
            return None
        except ValueError:
            print(cookies)
            return None