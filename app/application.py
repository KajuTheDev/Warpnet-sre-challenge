import sqlite3
import logging
from flask import Flask, session, redirect, url_for, request, render_template, abort


app = Flask(__name__)
app.secret_key = b"192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
app.logger.setLevel(logging.INFO)


def get_db_connection():
    try:
        connection = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as SQLerror:
        app.logger.error(f"Database connection error: {SQLerror}")
        abort(500)


def is_authenticated():
    return "username" in session
    # if "username" in session:
    #    return True
    # return False


def authenticate(username, password):
    connection = get_db_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    connection.close()

    if user and user["password"] == password:
        # app.logger.info(f"the user '{username}' logged in successfully with password '{password}'")
        app.logger.info(f"the user '{username}' logged in successfully")
        session["username"] = username
        return True

    # app.logger.warning(f"the user '{ username }' failed to log in '{ password }'")
    app.logger.warning(f"the user '{username}' failed to log in")
    abort(401)


@app.route("/")
def index():
    return render_template("index.html", is_authenticated=is_authenticated())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if authenticate(username, password):
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
