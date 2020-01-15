import os
import random
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

@app.route("/newroom", methods=["POST"])
@login_required
def newroom():
    """Makes new room number"""
    username = request.form.get("username")
    # Check if username is unique
    result = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
    if result:
        return apology("This username already exists")
    roomnumber = random.randint(00000, 99999)
    exists = db.execute("SELECT roomnumber FROM rooms WHERE roomnumber = :roomnumber ", roomnumber=roomnumber)
    while exists:
            roomnumber = random.randint(00000, 99999)
    db.execute("INSERT INTO users (roomnumber, username) VALUES(:roomnumber, :username)", username=username, roomnumber=roomnumber)
    return redirect("/board", roomnumber, username, )

@app.route("/existing", methods=["POST"])
@login_required
def existing():
    """Add player to room"""
    username = request.form.get("username")
    roomnumber = request.form.get("roomnumber")
    db.execute("INSERT INTO users (roomnumber, username) VALUES(:roomnumber, :username)", username=username, roomnumber=roomnumber)
    return render_template("board.html")

@app.route("/questions", methods=["GET", "POST"])
def question():
    # category, difficulty

    """Handles a new question"""
    # get the data from the API
    URL = 'https://opentdb.com/api.php?amount=1&type=multiple'
    data = requests.get(URL).json()

    # create a list and add the question
    q_a = []
    q_a.append(data["results"][0]["question"])

    # generate a random number for the place of the correct answer in the list
    getal = random.randrange(2, 6)
    
    # add the correct answer to session
    session['correct_answer'] = data["results"][0]["correct_answer"]
    
    # put all the wrong answers and the correct answer in the dict
    for i in range(2, 6):
        if i < getal:
            q_a.append(data["results"][0]["incorrect_answers"][i - 2])                  
        elif i > getal:
            q_a.append(data["results"][0]["incorrect_answers"][i - 3])                   
        else:
            q_a.append(data["results"][0]["correct_answer"])

    # return the template with the list (with the question and four possible answers)
    return render_template("questions.html", data=q_a)

@app.route("/answer_check", methods=["GET", "POST"])
def answer_check():
    # check if the given answer is the correct answer
    if session['correct_answer'] == request.form.get("your_answer"):
        return jsonify(True)
    else:
        return jsonify(False)

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
