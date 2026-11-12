import mysql.connector
import os

#funkcja połaczenia z bazą danych
def get_connection():

    return mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= os.environ.get('MYSQL'),
        database= "users"
    )