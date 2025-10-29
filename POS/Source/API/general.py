import mysql.connector
import bcrypt


connection = mysql.connector.connect(host="localhost",database="pos",user="root",password="root")
cursor = connection.cursor(prepared=True)

class Utils():
    @staticmethod
    def login(username,password):
        data = (username,)
        query = """SELECT userId,HashedPassword FROM Users WHERE username = %s"""
        
        cursor.execute(query,data)
        result = cursor.fetchall()

        print(result)