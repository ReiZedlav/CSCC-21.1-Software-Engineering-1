
#system needs 1 admin

import mysql.connector
import bcrypt
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "database": "pos",
    "user": "root",
    "password": "root",
}

try:
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    password = "administrator"
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    hashed_str = hashed_bytes.decode("utf-8")

    data = ("sudo", "L.", "kernel", "administrator", hashed_str, 1)

    query = """
        INSERT INTO Users (firstName, middleName, lastName, userName, HashedPassword, roleId)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, data)
    connection.commit()
    print("User inserted, id:", cursor.lastrowid)

except Error as e:
    print("MySQL error:", e)

finally:
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
