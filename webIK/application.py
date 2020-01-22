import os
import random
import urllib.request
import requests
import json

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


@app.route("/", methods=["GET"])
def homescreen():
    """Shows homescreen"""
    return render_template("homescreen.html")

@app.route("/newroom", methods=["GET", "POST"])
def newroom():
    """Makes new room number"""
    if request.method == "POST":
        username = request.form.get("username")
        category = request.form.get("category")

        # Check is username only contains letters or numbers
        for character in username:
            if not character.isalnum():
                return apology("The username may only contain numbers or letters")

        # Create a new roomnumber
        roomnumber = random.randint(00000, 99999)
        exists = db.execute("SELECT roomnumber FROM rooms WHERE roomnumber = :roomnumber ", roomnumber=roomnumber)
        while exists:
            roomnumber = random.randint(00000, 99999)

        # Get new player in database
        db.execute("INSERT INTO rooms (roomnumber, username, category, place, turn, turn_fixed) VALUES(:roomnumber, :username, :category, :place, :turn, :turn_fixed)",
                    username=username, roomnumber=roomnumber, category=category, place=1, turn=1, turn_fixed=1)

        # Show roomnumber
        flash("Your roomcode will be {}".format(roomnumber))
        return render_template("login.html")
    else:
        return render_template("newroom.html")

@app.route("/existingroom", methods=["GET", "POST"])
def existingroom():
    """Add player to room"""
    if request.method == "POST":
        username = request.form.get("username")
        roomnumber = request.form.get("roomnumber")

        # Check is username only contains letters or numbers
        for character in username:
            if not character.isalnum():
                return apology("The username may only contain numbers or letters")

        # Check if room exists and room is not full
        in_room = db.execute("SELECT username FROM rooms WHERE roomnumber = :roomnumber", roomnumber=roomnumber)
        if len(in_room) == 0:
            return apology("This room does not exist")
        elif len(in_room) == 4:
            return apology("This room already contains the maximum of 4 players")

        turn = len(in_room) + 1
        result = db.execute("SELECT username FROM rooms WHERE roomnumber = :roomnumber AND username= :username", roomnumber=roomnumber, username=username)
        if not result:
            category = db.execute("SELECT category FROM rooms WHERE roomnumber = :roomnumber", roomnumber=roomnumber)[0]['category']
            db.execute("INSERT INTO rooms (roomnumber, username, place, turn, category, turn_fixed) VALUES(:roomnumber, :username, :place, :turn, :category, :turn_fixed)",
                        username=username, roomnumber=roomnumber, place=1, turn=turn, category=category, turn_fixed=turn)
        else:
            return apology("This username already exists in this room, use log in")
        return redirect("/board")
    else:
        return render_template("existingroom.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log player in to show board"""
    if request.method == "POST":
        username = request.form.get("username")
        roomnumber = request.form.get("roomnumber")

        # Username and password have to be filled in
        if not username or not roomnumber:
            return apology("must provide username and password", 403)

        rows = db.execute("SELECT * FROM rooms WHERE username = :username AND roomnumber= :roomnumber", username=username, roomnumber=roomnumber)

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return apology("invalid username and/or roomname", 403)

        # Set new timestamp and log user in
        session["user_id"] = rows[0]["user_id"]
        db.execute("UPDATE rooms SET date = current_timestamp WHERE user_id = :user_id", user_id=session["user_id"])
        return redirect("/board")
    else:
        return render_template("login.html")

@app.route("/questions", methods=["GET", "POST"])
@login_required
def question():
    """Handles a new question"""
    # get the difficulty for this player from database
    difficulty = str(db.execute("SELECT category FROM rooms WHERE roomnumber = :roomnumber AND username= :username",
                    roomnumber=request.form.get("roomnumber"), username=request.form.get("username")))

    # Get the questions and answer(s) from API
    URL = str('https://opentdb.com/api.php?amount=1&difficulty=' + difficulty + '&type=multiple')
    data = requests.get(URL).json()

    # Choose the place for the right answer
    getal = random.randrange(2, 6)

    # Create list with the question[0], and 4 possible answers in random order
    q_a = []
    q_a.append(str(data["results"][0]["question"]))

    # To make sure the right letter (for the right answer) is saved
    answer_converter = {1:'A', 2:'B', 3:'C', 4:'D'}

    # Makes a list with 3 wrong answers and a good answer in a random order
    for i in range(2, 6):
        if i < getal:
            q_a.append(data["results"][0]["incorrect_answers"][i - 2])

        elif i > getal:
            q_a.append(data["results"][0]["incorrect_answers"][i - 3])

        else:
            q_a.append(data["results"][0]["correct_answer"])
            # Saves right answer (A, B, C or D) in the session
            session["correct_answer"] = answer_converter[i - 1]

    # Return template with the list [q, aA, aB, aC, aD] with one of them correct (and saved in session)
    return render_template("questions.html", data=q_a)

@app.route("/answer_check", methods=["GET"])
@login_required
def answer_check():
    """Checks if question is answered correctly"""
    # return jsonify(session["correct_answer"] != request.form.get('your_answer'))
    # return jsonify(True)
    if session["correct_answer"] == request.form.get('your_answer'):
        db.execute("UPDATE rooms SET place = place + :place WHERE user_id = :user_id", user_id=session["user_id"], place=1)
        flash("Yes, you gave the correct answer! :)")
        # return jsonify(True)
    else:
        flash("Aww, unfortunately that's not the correct answer :(")
        # return jsonify(False)
    return redirect("/board")

@app.route("/board")
# @login_required
def board():
    """Handles a new question"""

    playerdata = db.execute("SELECT roomnumber, username, place, turn, turn_fixed FROM rooms WHERE user_id = :user_id",
                                user_id=session["user_id"])

    boarddata = db.execute("SELECT username, place, turn, turn_fixed FROM rooms WHERE roomnumber = :roomnumber GROUP BY turn_fixed",
                                roomnumber=playerdata[0]["roomnumber"])

    boarddatajs = json.dumps(boarddata)

    return render_template("board.html",
                            boarddata=boarddata,
                            playerdata=playerdata,
                            boarddatajs=boarddatajs)

@app.route("/roll_dice")
# @login_required
def roll_dice():

    playerdata = request.args.get('playerdata', '')

    print("playerdata:", playerdata)

    dobbelsteen = random.randrange(1,4,1)

    db.execute("UPDATE rooms SET place = place + :dobbelsteen WHERE roomnumber = :roomnumber AND username = :username",
                roomnumber=playerdata[0]["roomnumber"],
                username=playerdata[0]["username"],
                dobbelsteen=dobbelsteen)

    # TODO:
    # Plaats hier code om een vraag te beantwoorden of redirect daar naar toe
    #

    return redirect("/compute_turn")

@app.route("/compute_turn")
# @login_required
def compute_turn():

    playerdata = db.execute("SELECT roomnumber, username, place, turn FROM rooms WHERE user_id = :user_id",
                                user_id=session["user_id"])

    boarddata = db.execute("SELECT username, place, turn FROM rooms WHERE roomnumber = :roomnumber GROUP BY username",
                                    roomnumber=playerdata[0]["roomnumber"])

    current_player = playerdata[0]["username"]

    for otherplayer in boarddata:

        if otherplayer["username"] != current_player:

            db.execute("UPDATE rooms SET turn = turn - 1 WHERE username = :username",
                        username=otherplayer["username"])

        else:

            db.execute("UPDATE rooms SET turn = 4 WHERE username = :username",
                        username=current_player)

    return redirect("/board")


@app.route("/viewboard")
# @login_required
def viewboard():

    return render_template("board.html")

@app.route("/winner", methods=["POST"])
# @login_required
def winner():
    return render_template("winner.html")

@app.route("/loser", methods=["POST"])
# @login_required
def loser():
    return render_template("loser.html")

@app.route("/logout")
def logout():
    """log user out"""
    session.clear()
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return print(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
