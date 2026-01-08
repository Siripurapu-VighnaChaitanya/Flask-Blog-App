from flask import Flask,render_template,redirect,request,session,url_for
from auth import auth_bp
from blog import blog_bp

app=Flask(__name__)
app.secret_key="my_secret_key"

app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)

@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()