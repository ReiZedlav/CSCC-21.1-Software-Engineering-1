from PIL import Image
import mysql.connector
import bcrypt
import calendar
import datetime
import os

#everything thats not administrative or used by cashier belongs here.

connection = mysql.connector.connect(host="localhost",database="pos",user="root",password="")
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
        with open(f"../Receipts/{filename}.txt", "w") as file:
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
    def login(username, password):
        data = (username,)
        query = """SELECT userId, roleId, HashedPassword FROM Users WHERE username = %s"""
        
        cursor.execute(query, data)
        result = cursor.fetchall()


        if not result:
            return None

        try:
            user_id = result[0][0]
            role_id = result[0][1]
            bcryptPassword = result[0][2]
            
            print(f"User ID: {user_id}")
            print(f"Role ID: {role_id}") 
            print(f"Stored password: {bcryptPassword}")
            print(f"Input password: {password}")
            
            if not bcryptPassword:
                return None
            
            print(f"Password type: {type(bcryptPassword)}")
            print(f"Password encoded: {bcryptPassword.encode('utf-8')}")
            
            verified = bcrypt.checkpw(password.encode('utf-8'), bcryptPassword.encode('utf-8'))
            
            print(f"Password verified: {verified}")
            
            if verified:
                cookies = {
                    "userID": user_id,
                    "roleID": role_id
                }
                print(f"Login successful: {cookies}")
                return cookies
            else:
                print("Password verification failed")
                return None
            
        except ValueError as e:
            print(f"Value error details: {e}")
            print(f"Error type: {type(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return None