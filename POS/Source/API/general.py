import mysql.connector
import bcrypt


connection = mysql.connector.connect(host="localhost",database="pos",user="root",password="root")
cursor = connection.cursor(prepared=True)

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
            print("User not found!")

        try:
            verified = bcrypt.checkpw(password.encode('utf-8'),bcryptPassword.encode('utf-8'))
            
            if verified:
                #login to cashier or admin panel based on role.
                print("success")

                #if roleid = 1 -> admin
                #if roleid = 2 -? cashier


                pass
            else:
                print("Wrong username or password!")
            
        except UnboundLocalError:
            pass
        except ValueError:
            pass
