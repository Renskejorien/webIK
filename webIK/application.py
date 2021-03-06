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
from helpers import login_required, apology, add_player, delete_player, player_data, board_data
from datetime import datetime, timedelta

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

@app.route("/newroom/", methods=["GET", "POST"])
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
        while db.execute("SELECT roomnumber FROM rooms WHERE roomnumber = :roomnumber ", roomnumber=roomnumber):
            roomnumber = random.randint(00000, 99999)

        turn = 1
        turn_fixed = turn
        date = datetime.timestamp(datetime.now())
        rolled = 0

        # Get new player in database
        add_player(username, roomnumber, turn, category, turn_fixed, date, rolled)

        # Show roomnumber
        flash("Your roomcode will be {}".format(roomnumber))
        return render_template("login.html")
    return render_template("newroom.html")

@app.route("/existingroom/", methods=["GET", "POST"])
def existingroom():
    """Add player to an existing room"""
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
        turn_fixed = turn
        date = datetime.timestamp(datetime.now())
        rolled = 0

        result = db.execute("SELECT username FROM rooms WHERE roomnumber = :roomnumber AND username= :username", roomnumber=roomnumber, username=username)
        if not result:
            category = db.execute("SELECT category FROM rooms WHERE roomnumber = :roomnumber", roomnumber=roomnumber)[0]['category']
            add_player(username, roomnumber, turn, category, turn_fixed, date, rolled)
        else:
            return apology("This username already exists in this room, use log in")
        rows = db.execute("SELECT * FROM rooms WHERE username = :username AND roomnumber= :roomnumber", username=username, roomnumber=roomnumber)
        session["user_id"] = rows[0]["user_id"]
        return redirect("/board/")
    return render_template("existingroom.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    """Log player in to show board"""
    if request.method == "POST":
        username = request.form.get("username")
        roomnumber = request.form.get("roomnumber")

        # Username and password have to be filled in
        if not username or not roomnumber:
            return apology("must provide username and password")

        rows = db.execute("SELECT * FROM rooms WHERE username = :username AND roomnumber= :roomnumber", username=username, roomnumber=roomnumber)

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return apology("invalid username and/or roomname")

        # Set new timestamp and log user in
        session["user_id"] = rows[0]["user_id"]
        date = datetime.timestamp(datetime.now())
        db.execute("UPDATE rooms SET date = :date WHERE user_id = :user_id", user_id=session["user_id"], date=date)
        return redirect("/board/")
    return render_template("login.html")

@app.route("/questions/", methods=["GET", "POST"])
@login_required
def question():
    """Handles a new question"""
    # Check if it's your turn
    if player_data(session["user_id"])[0]['turn'] == 1:

        # Get the place for this player from database
        place = int(player_data(session["user_id"])[0]['place'])

        # Pick the category that matches the players board-position
        if place % 4 == 0:
            category = '17' #  science & nature
        elif (place + 1) % 4 == 0:
            category = '21' # sports
        elif (place + 2) % 4 == 0:
            category = '22' # geography
        else:
            category = '23' # history

        # Get the difficulty for this player from database
        difficulty = str(player_data(session["user_id"])[0]['category'])

        # Get the questions and answer(s) from API
        URL = str('https://opentdb.com/api.php?amount=1&category=' + category + '&difficulty=' + difficulty + '&type=multiple')
        data = requests.get(URL).json()

        # Choose the place for the right answer
        answer_place = random.randrange(2, 6)

        # Create list with the question[0], and 4 possible answers in random order
        q_a = []
        q_a.append(str(data["results"][0]["question"]))

        # To make sure the right letter (for the right answer) is saved
        answer_converter = {1:'A', 2:'B', 3:'C', 4:'D'}

        # Makes a list with 3 wrong answers and a good answer in a random order
        for i in range(2, 6):
            if i < answer_place:
                q_a.append(data["results"][0]["incorrect_answers"][i - 2])
            elif i > answer_place:
                q_a.append(data["results"][0]["incorrect_answers"][i - 3])
            else:
                q_a.append(data["results"][0]["correct_answer"])
                # Saves right answer (A, B, C or D) in the session
                session["correct_answer"] = answer_converter[i - 1]

        # Return template with the list [q, aA, aB, aC, aD] with one of them correct (and saved in session)
        return render_template("questions.html", data=q_a)
    return redirect("/board/")


@app.route("/answer_check/", methods=["GET"])
@login_required
def answer_check():
    """Checks if question is answered correctly"""

    # If you gave the correct answer, update new place and return true
    if session["correct_answer"] == request.args.get('your_answer'):
        db.execute("UPDATE rooms SET place = place + :place WHERE user_id = :user_id", user_id=session["user_id"], place=1)
        return jsonify(True)
    return jsonify(False)

@app.route("/board/")
@login_required
def board():
    """Shows the board and the location of the players"""
    playerdata = player_data(session["user_id"])
    roomnumber = int(playerdata[0]["roomnumber"])
    boarddata = board_data(roomnumber)

    # Check if the is supposed to be in the bridge
    if playerdata[0]["in_bridge"] == 1:
        return redirect("/bridge/")

    # If a player takes longer than one day to complete their turn, delete player
    for player in boarddata:
        if player["date"] <= datetime.timestamp(datetime.now() - timedelta(days=1)):
            delete_player(player, playerdata)

    # Checks if player is on a risky place
    if playerdata[0]["place"] == 5 or playerdata[0]["place"] == 12:
        risky = True
    else:
        risky = False

    # Checks if the game is won
    if playerdata[0]["won"] == 1:
        if playerdata[0]["place"] >= 18:
            return render_template("winner.html")
        return render_template("loser.html")

    # Checks if it's the players turn
    if int(playerdata[0]["turn"]) == 1:
        playerturn = True
    else:
        playerturn = False

    roomnumber = int(playerdata[0]["roomnumber"])
    boarddatajs = json.dumps(boarddata)
    return render_template("board.html", playerturn=playerturn, boarddatajs=boarddatajs, roomnumber=roomnumber,
                            boarddata=boarddata, risky=risky, explanation=int(playerdata[0]["won"]))

@app.route("/bridge/")
@login_required
def bridge():
    """After a player rolls dice, they can press the button to see the question"""
    playerdata = player_data(session["user_id"])
    roomnumber = int(playerdata[0]["roomnumber"])
    boarddata = board_data(roomnumber)

    db.execute("UPDATE rooms SET in_bridge = 1, won = 0 WHERE user_id = :user_id",
                    user_id=session["user_id"])

    # If a player reaches the finish, set won
    if int(playerdata[0]["place"]) >= 18:
            db.execute("UPDATE rooms SET won = :won WHERE roomnumber = :roomnumber",
                    roomnumber=playerdata[0]["roomnumber"], won=1)

    # Checks if the game is won and by who
    if playerdata[0]["won"] == 1:
        if playerdata[0]["place"] >= 18:
            return render_template("winner.html")
        return render_template("loser.html")

    roomnumber = int(playerdata[0]["roomnumber"])
    boarddatajs = json.dumps(boarddata)
    rolled = int(playerdata[0]["rolled"])

    return render_template("board.html", boarddatajs=boarddatajs, roomnumber=roomnumber,boarddata=boarddata,
                            to_question=True, rolled=rolled)

@app.route("/roll_dice/", methods=["GET"])
@login_required
def roll_dice():
    """Roll dice if it's a players turn"""
    playerdata = player_data(session["user_id"])
    roomnumber = int(playerdata[0]["roomnumber"])

    # The player can only roll dice if it's their turn
    if int(playerdata[0]["turn"]) == 1:

        # Checks if player is on a risky box and replaces dice if so
        if playerdata[0]["place"] == 5 or playerdata[0]["place"] == 12:
            choice = [-2, 1]
            dice = random.choice(choice)
            db.execute("UPDATE rooms SET place = place + :dice, rolled = :dice WHERE roomnumber = :roomnumber AND user_id = :user_id",
                        roomnumber=roomnumber, user_id=session["user_id"], dice=dice)
        else:
            dice = random.randrange(1,3,1)
            db.execute("UPDATE rooms SET place = place + :dice, rolled = :dice WHERE roomnumber = :roomnumber AND user_id = :user_id",
                        roomnumber=roomnumber, user_id=session["user_id"], dice=dice)

    return redirect("/bridge/")

@app.route("/compute_turn/")
@login_required
def compute_turn():
    """Set new turn for each player"""
    db.execute("UPDATE rooms SET in_bridge = 0, rolled = 0 WHERE user_id = :user_id",
                    user_id=session["user_id"])

    playerdata = player_data(session["user_id"])
    roomnumber = int(playerdata[0]["roomnumber"])

    # Can only compute turn if it's the players turn
    if int(playerdata[0]["turn"]) == 1:

        # If a player reaches the finish, the game is over
        if int(playerdata[0]["place"]) >= 18:
            db.execute("UPDATE rooms SET won = :won WHERE roomnumber = :roomnumber",
                        roomnumber=roomnumber, won=1)
        boarddata = board_data(roomnumber)

        # Set the new turn for each player
        current_player = playerdata[0]["username"]
        for otherplayer in boarddata:
            if otherplayer["username"] != current_player:
                db.execute("UPDATE rooms SET turn = turn - 1 WHERE username = :username",
                            username=otherplayer["username"])
            else:
                l = len(boarddata)
                db.execute("UPDATE rooms SET turn = :l WHERE username = :username",
                            username=current_player, l=l)
    return redirect("/board/")

@app.route("/logout/")
def logout():
    """Log user out"""
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
