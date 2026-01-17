from flask import Flask,render_template,redirect,request,session,url_for
from auth import auth_bp
from blog import blog_bp
from modules.db import new_connection

app=Flask(__name__)
app.secret_key="my_secret_key"

app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)

@app.route("/")
def home():
    return render_template("base.html")

def init_db():
    conn = new_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)