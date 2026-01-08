from flask import Flask,redirect,render_template,flash,url_for,request,session
from modules.db import new_connection
from werkzeug.security import generate_password_hash,check_password_hash
from auth import auth_bp
from blog import blog_bp

@auth_bp.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        hashed_password=generate_password_hash(password)

        conn=new_connection()
        cursor=conn.cursor()
        query="INSERT INTO users(name,email,password) VALUES(%s,%s,%s)"
        values=(name,email,hashed_password)
        cursor.execute(query,values)
        conn.commit()
        conn.close()
        cursor.close()

        flash("Registration Successful Pls Login...","Success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        conn=new_connection()
        cursor=conn.cursor()
        query="SELECT * FROM users WHERE email=%s"
        values=(email,)
        cursor.execute(query,values)
        data=cursor.fetchone()
        cursor.close()
        conn.close()

        if data and check_password_hash(data[3],password):
            session["user_id"]=data[0]
            session["user_name"]=data[1]
            return redirect(url_for("blog.dashboard"))
        else:
            flash("invalid email or password ....","danger")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout successfully.....","success")
    return redirect(url_for("auth.login"))
