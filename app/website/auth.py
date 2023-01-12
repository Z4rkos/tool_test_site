from flask import Blueprint, render_template, request, flash, redirect, make_response
from .db import *
from . import app
import jwt

auth = Blueprint('auth', __name__)


@auth.route("login", methods=["GET", "POST"])
def login():
    user = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user_id(username)
        if user:
            if check_credentials(username, password):
                flash(f"Logged in!", category="success")
                resp = make_response(redirect("/"))

                resp.set_cookie("jwt", jwt.encode(
                    {'username': username},
                    app.config["SECRET_KEY"],
                    algorithm=app.config['ALGORITHM']
                ))

                return resp

            else:
                flash("Incorrect password.", category="error")
        else:
            flash("Incorrect username.", category="error")

    return render_template("login.html", user=user)


@auth.route("logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.set_cookie("jwt", "", expires=0)
    return resp


@auth.route("register", methods=["GET", "POST"])
def register():
    user = ""
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Validation checks
        if len(email) < 4:
            flash("Email must be atleast 4 characters", category="error")
        elif len(username) < 2:
            flash("Username must be two or more characters.", category="error")
        elif len(password1) < 8:
            flash("Password must be 8 or more characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        else:
            user = get_user_id(username)
            if user:
                flash("Username allready in use", category="error")
                user = ""
            else:
                register_user(username, password1, email)

                flash("Account created successfully!", category="success")

                resp = make_response(redirect("/"))
                resp.set_cookie("jwt", jwt.encode(
                    {'username': username},
                    app.config["SECRET_KEY"],
                    algorithm=app.config['ALGORITHM']
                ))
                return resp

    return render_template("register.html", user=user)
