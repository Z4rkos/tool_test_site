from . import db_connection

con = db_connection()
cursor = con.cursor()

"""
Didn't really have to make everything here vulnerable, but I felt like it made sense.
It's like a theme, everything is horrible :P
"""


def get_user_id(username) -> str:
    """
    Gets a user_id from the database based on username.
    Returns the user_id if the username is in the system, if not it return an empty string.
    """
    cursor.execute(
        f"SELECT user_id FROM Users WHERE username='{username}'"
    )
    data = cursor.fetchone()

    user_id = ""
    if data:
        user_id = data.get("user_id")

    return user_id


def register_user(username, password, email):
    """
    Registers a user by inserting them into the database.
    Should maybe add some error handeling and return a message here.
    """

    cursor.execute(
        f"INSERT INTO Users (username, password, email) VALUES('{username}', '{password}', '{email}')"
    )
    con.commit()


def check_credentials(username, password) -> bool:
    """
    Checks if the username and password combination exists in the database.
    Returns True if it does, else False.
    """
    cursor.execute(
        f"SELECT * from Users WHERE username='{username}' AND password='{password}'"
    )
    user = cursor.fetchone()
    if user:
        return True
    return False


def get_posts_category(category) -> list:
    """
    Gets notes from the database based on user_id.
    Formats the notes so they are in a list, then returns them.
    """
    if category == "all":
        cursor.execute(
            f"SELECT title, data, category, username FROM Posts"
        )
    else:
        cursor.execute(
            f"SELECT title, data, category, username FROM Posts WHERE category='{category}'"
        )
    posts = cursor.fetchall()

    return posts


def new_post(title, data, category, username):
    """
    Inserts a new post into the database.
    """
    cursor.execute(
        f'INSERT INTO Posts (title, data, category, username) VALUES("{title}", "{data}", "{category}", "{username}")'
    )
    con.commit()


def get_categories():
    cursor.execute(
        f"SELECT DISTINCT category FROM Posts"
    )
    categories = cursor.fetchall()

    return categories
