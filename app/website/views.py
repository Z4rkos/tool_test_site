from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from .db import get_posts_category, new_post, get_categories
import jwt
from . import app

# A blueprint is basically a collection of routes
views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
def home():

    auth_cookie = request.cookies.get("jwt")
    if auth_cookie:
        try:
            username = jwt.decode(
                auth_cookie, key=app.config["SECRET_KEY"], algorithms=app.config["ALGORITHM"]).get("username")

            category = request.args.get("category")
            all_categories = get_categories()
            if category:
                posts = get_posts_category(category=category)
            else:
                posts = get_posts_category("all")
            return render_template("home.html", user=username, posts=posts, categories=all_categories)

        except jwt.exceptions.InvalidSignatureError:
            flash("Invalid Cookie!", category="error")
            return redirect(url_for('auth.login'))

    else:
        return redirect(url_for('auth.login'))


@app.route("/new_post", methods=["GET", "POST"])
def modal():

    category = request.args.get("category")
    all_categories = get_categories()

    if category:
        posts = get_posts_category(category=category)
    else:
        posts = get_posts_category("all")

    username = ""
    auth_cookie = request.cookies.get("jwt")

    try:
        username = jwt.decode(
            auth_cookie, key=app.config["SECRET_KEY"], algorithms=app.config["ALGORITHM"]).get("username")
    except jwt.exceptions.InvalidSignatureError:
        flash("Invalid Cookie!", category="error")
        resp = make_response(redirect("/login"))
        resp.set_cookie("jwt", "", expires=0)
        return resp

    if request.method == "POST":

        title = request.form.get("title")
        data = request.form.get("data")
        category = request.form.get("category")
        username = request.form.get("username")

        if len(data) < 1:
            flash("Post too short", category="error")
        elif not title:
            flash("Please include a title", category="error")
        elif not category:
            flash("Please include a category", category="error")
        else:
            new_post(title, data, category, username)
            flash("Post created!", category="success")
            return redirect(url_for('views.home'))

    return render_template("post_modal.html", posts=posts, categories=all_categories, user=username)
