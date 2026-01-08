import mysql.connector

def new_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chaitanya659328@+",
        database="blog_db"
    )
