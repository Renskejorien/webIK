import os
import random
import urllib.request
import requests

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
        username = request.form.get("username")
        category = request.form.get("category")
        roomnumber = random.randint(00000, 99999)
        exists = db.execute("SELECT roomnumber FROM rooms WHERE roomnumber = :roomnumber ", roomnumber=roomnumber)
        while exists:
            roomnumber = random.randint(00000, 99999)
        db.execute("INSERT INTO rooms (roomnumber, username, category, place, turn) VALUES(:roomnumber, :username, :category, :place, :turn)",
                    username=username, roomnumber=roomnumber, category=category, place=1, turn=1)
        return redirect("/viewboard")
    else:
        return render_template("newroom.html")

@app.route("/existingroom", methods=["GET", "POST"])
def existingroom():
    """Add player to room"""
    if request.method == "POST":
        username = request.form.get("username")
        roomnumber = request.form.get("roomnumber")
        # Check if username is unique
        result = db.execute("SELECT username FROM rooms WHERE roomnumber = :roomnumber AND username= :username", roomnumber=roomnumber, username=username)
        print(username, result)
        if result:
            return apology("This username already exists in this room")
        in_room = db.execute("SELECT username FROM rooms WHERE roomnumber = :roomnumber", roomnumber=roomnumber)
        if len(in_room) == 0:
            return apology("This room does not exist")
        turn = len(in_room) + 1
        db.execute("INSERT INTO rooms (roomnumber, username, place, turn) VALUES(:roomnumber, :username, :place, :turn)",
                    username=username, roomnumber=roomnumber, place=1, turn=turn)
        return redirect("/viewboard")
    else:
        return render_template("existingroom.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Add player to room"""
    if request.method == "POST":
        username = request.form.get("username")
        roomnumber = request.form.get("roomnumber")
        if not username or not roomnumber:
            return apology("must provide username and password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM rooms WHERE username = :username AND roomnumber= :roomnumber", username=username, roomnumber=roomnumber)

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return apology("invalid username and/or roomname", 403)
        session["user_id"] = rows[0]["user_id"]
        return redirect("/viewboard")
    else:
        return render_template("login.html")

@app.route("/questions", methods=["GET", "POST"])
def question():
    """Handles a new question"""
    URL = 'https://opentdb.com/api.php?amount=1&type=multiple'
    data = requests.get(URL).json()
    getal = random.randrange(2, 6)
    q_a = []
    q_a.append(data["results"][0]["question"])
    # q_a.append(data["results"][0]["correct_answer"])

    for i in range(2, 6):
        if i < getal:
            q_a.append(data["results"][0]["incorrect_answers"][i - 2])

        elif i > getal:
            q_a.append(data["results"][0]["incorrect_answers"][i - 3])

        else:
            q_a.append(data["results"][0]["correct_answer"])
    return data
    # return render_template("questions.html")

@app.route("/board")
def board():
    """Handles a new question"""

    #
    #
    # DIT KLOPT NOG NIET, VIND MOGELIJKHEID OM DEZE VARIABELEN TE VERKRIJGEN
    #
    # waarchijnlijk met request.form.get("username")

    roomnumber = request.args.get('username', '')

    username = request.args.get('wa8w', '')

    #
    #
    #
    #
    #

    if roomnumber and username:

        boarddata = db.execute("SELECT username, place, turn FROM rooms WHERE roomnumber = :roomnumber GROUP BY username",
                                    roomnumber=roomnumber)

        # Vergeet bij deze twee niet turn_fixed toe te voegen!

        playerdata = db.execute("SELECT username, place, turn FROM rooms WHERE roomnumber = :roomnumber AND username = :username",
                                    roomnumber=roomnumber,
                                    username=username)

        return render_template("board.html",
                                boarddata=boarddata,
                                playerdata=playerdata)

    else:

        redirect("/")

@app.route("/turn")
def compute_turn():

    #
    #
    # DIT KLOPT NOG NIET, VIND MOGELIJKHEID OM DEZE VARIABELEN TE VERKRIJGEN
    #
    # waarschijnlijk via js

    current_player = request.args.get('username', '')

    place = request.args.get('place', '')

    roomnumber = request.args.get('DitIsNietDeManier', '')

    # behalve roomnumber, fijn als die eigenlijk altijd aanwezig is, zoals een session id
    #
    #
    #
    #

    boarddata = db.execute("SELECT username, place, turn FROM rooms WHERE roomnumber = :roomnumber GROUP BY username",
                                    roomnumber=roomnumber)

    for otherplayer in boarddata:

        if otherplayer["username"] != current_player:

            db.execute("UPDATE rooms SET turn = turn - 1 WHERE username = :username",
                        username=otherplayer["username"])

        else:

            db.execute("UPDATE rooms SET turn = 4 WHERE username = :username",
                        username=current_player)

            db.execute("UPDATE rooms SET place = :place WHERE username = :username",
                        username=current_player,
                        place=place)

    redirect


@app.route("/viewboard")
def viewboard():

    return render_template("board.html")

@app.route("/winner", methods=["POST"])
def winner():
    return render_template("winner.html")

@app.route("/loser", methods=["POST"])
def loser():
    return render_template("loser.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return print(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
