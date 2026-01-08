import mysql.connector

def new_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="******",
        database="blog_db"
    )
