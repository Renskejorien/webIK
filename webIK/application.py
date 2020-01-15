import os
import random
import urllib

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

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

@app.route("/newroom", methods=["GET", "POST"])
def newroom():
    """Makes new room number"""
    if request.method == "POST":
        print("hoi")
        username = request.form.get("username")
        # Check if username is unique
        result = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if result:
            return apology("This username already exists")
        roomnumber = random.randint(00000, 99999)
        exists = db.execute("SELECT roomnumber FROM rooms WHERE roomnumber = :roomnumber ", roomnumber=roomnumber)
        while exists:
                roomnumber = random.randint(00000, 99999)
        db.execute("INSERT INTO users (roomnumber, username, place, turn) VALUES(:roomnumber, :username, :place, :turn)", username=username, roomnumber=roomnumber, place=1, turn=1)
        return redirect("/board", roomnumber, username)
    else:
        return render_template("newroom.html")

@app.route("/existing", methods=["POST"])
@login_required
def existing():
    """Add player to room"""
    username = request.form.get("username")
    roomnumber = request.form.get("roomnumber")
    in_room = db.execute("SELECT username FROM rooms WHERE roomnumber = :roomnumber", roomnumber=roomnumber)
    turn = len(in_room) + 1
    db.execute("INSERT INTO users (roomnumber, username, place, turn) VALUES(:roomnumber, :username, :place, :turn)", username=username, roomnumber=roomnumber, place=1, turn=turn)
    return redirect("/board", roomnumber, username)

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
