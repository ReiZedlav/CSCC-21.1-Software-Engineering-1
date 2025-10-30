import mysql.connector
import bcrypt
from mysql.connector import Error

# --- Config ---
DB_CONFIG = {
    "host": "localhost",
    "database": "pos",
    "user": "root",
    "password": "root",
}

try:
    # connect
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # password hashing (bcrypt returns bytes)
    password = "administrator"
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    # decode to store as text (bcrypt output is ASCII-safe)
    hashed_str = hashed_bytes.decode("utf-8")

    # data to insert (order matches columns)
    data = ("sudo", "L.", "kernel", "administrator", hashed_str, 1)

    # SQL with the correct number of placeholders
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
