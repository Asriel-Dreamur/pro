from flask import Flask, render_template, request, session, redirect

from user import create_user_table, User
from post import create_post_table, Post

import secrets

create_post_table()
create_user_table()

app = Flask("main")
app.secret_key = secrets.token_hex(32)


@app.route("/")
def index_page():
    posts = Post.get_all()

    username = session.get("username", None)
    user = None
    if username:
        user = User.get_user_by_username(username)

    return render_template("index.html", posts=posts, user=user)


@app.route("/registration", methods=["POST", "GET"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.get_user_by_username(username)
        if user:
            return render_template(
                "register.html", error="Пользователь с таким ником уже есть"
            )
        
        if password != confirm_password:
            return render_template(
                "register.html", error="Пароли не совпадают"
            )
        
        User.create(username, password)
        session["username"] = username
        return redirect('/')
        


@app.route("/login")
def login_page():
    return


@app.route("/profile")
def profile_page():
    return


app.run(host="0.0.0.0", port=8080)