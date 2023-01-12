from flask import Flask
from flask_mysqldb import MySQL


# Initiates Flask
app = Flask(__name__)
app.app_context().push()


def create_app():

    # Secret key that will be used for encrypting session data and cookies. The key is in rockyou.txt :P
    app.config['SECRET_KEY'] = '88206023'
    app.config['ALGORITHM'] = "HS256"

    # Import and register blueprints.
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    init_db()

    return app


def db_connection(app=app):

    # This stuff would normally be in a .env file, but nice to make it extra insecure.
    app.config['MYSQL_HOST'] = 'db'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'db'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)

    con = mysql.connect

    return con


def init_db():
    con = db_connection()
    cursor = con.cursor()

    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS db;"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Users (user_id INT AUTO_INCREMENT PRIMARY KEY, username TEXT, password TEXT, email TEXT);"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Posts (id INT AUTO_INCREMENT PRIMARY KEY, title TEXT, data TEXT, category TEXT, username TEXT);"
    )

    con.commit()
