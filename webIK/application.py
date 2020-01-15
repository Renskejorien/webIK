import os
import random
import urllib

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///spel.db")


@app.route("/", methods=["GET", "POST"])
def homescreen():
    """Shows homescreen"""
    if request.method == "GET":
        return render_template("homescreen.html")

@app.route("/newroom", methods=["POST"])
@login_required
def newroom():
    """Makes new room number"""
    username = request.form.get("username")
    roomnumber = random.randint(00000, 99999)
    exists = db.execute("SELECT roomnumber FROM rooms WHERE roomnumber = :roomnumber ", roomnumber=roomnumber)
    while exists:
            roomnumber = random.randint(00000, 99999)
    db.execute("INSERT INTO users (roomnumber, username) VALUES(:roomnumber, :username)", username=username, roomnumber=roomnumber)
    return render_template("board.html")

@app.route("/existing", methods=["POST"])
@login_required
def existing():
    """Add player to room"""
    username = request.form.get("username")
    roomnumber = request.form.get("roomnumber")
    db.execute("INSERT INTO users (roomnumber, username) VALUES(:roomnumber, :username)", username=username, roomnumber=roomnumber)
    return render_template("board.html")

@app.route("/questions", methods=["GET", "POST"])
def question(category, difficulty):
    

    """Handles a new question"""
    URL = 'https://opentdb.com/api.php?amount=1&type=multiple'
    data = urllib.urlopen(URL).read()
    print(data)

    return render_template("questions.html")

@app.route("/board")
def board():
    """Handles a new question"""

    return render_template("board.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return print(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
