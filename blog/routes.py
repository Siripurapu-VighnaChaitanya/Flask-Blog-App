from flask import Flask,session,redirect,url_for,render_template,request
from modules.db import new_connection
from blog import blog_bp
from functools import wraps

def login_check(func):
    @wraps(func)
    def wrapper(*args,**kargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return func(*args,**kargs)
    return wrapper

@blog_bp.route("/dashboard")
@login_check
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")

@blog_bp.route("/create_post",methods=["GET","POST"])
@login_check
def create_post():
    if request.method=="POST":
        title=request.form.get("title")
        content=request.form.get("content")
        user_id=session["user_id"]
        conn=new_connection()
        cursor=conn.cursor()
        query="INSERT INTO posts(title,content,user_id) VALUES(%s,%s,%s)"
        values=(title,content,user_id)
        cursor.execute(query,values)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("blog.posts"))
    return render_template("create_post.html")

@blog_bp.route("/posts")
def posts():
    conn=new_connection()
    cursor=conn.cursor(dictionary=True)
    query="SELECT posts.id,posts.title,posts.content,users.name,posts.created_at,posts.user_id FROM posts INNER JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC"
    cursor.execute(query)
    all_posts=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("posts.html",posts=all_posts)

@blog_bp.route("/update/<int:id>",methods=["GET","POST"])
@login_check
def update(id):
    conn=new_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id=%s",(id,))
    data=cursor.fetchone()

    if not data:
        cursor.close()
        conn.close()
        return "Data not found ",404
    
    if data["user_id"] != session["user_id"]:
        cursor.close()
        conn.close()
        return "Unauthorized ",403
    

    if request.method=="POST":
        title=request.form.get("title")
        content=request.form.get("content")
        query="UPDATE posts SET title=%s,content=%s WHERE id=%s"
        values=(title,content,id)
        cursor.execute(query,values)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("blog.posts"))
    cursor.close()
    conn.close()
    return render_template("update_post.html",post=data)

@blog_bp.route("/delete/<int:id>")
@login_check
def delete_post(id):
    conn = new_connection()
    cursor = conn.cursor(dictionary=True)

    # get post
    cursor.execute("SELECT * FROM posts WHERE id=%s", (id,))
    post = cursor.fetchone()

    if not post:
        cursor.close()
        conn.close()
        return "Post not found", 404

    # ownership check
    if post["user_id"] != session["user_id"]:
        cursor.close()
        conn.close()
        return "Unauthorized", 403

    # delete post
    cursor.execute("DELETE FROM posts WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("blog.posts"))
