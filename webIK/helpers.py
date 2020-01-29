import requests
import urllib.parse
import os

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps

db = SQL("sqlite:///spel.db")

# Define a function that requires to be logged in
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Define a function that returns an html page with a spcecific message and errorcode
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

# Define a function that adds a player to a specific room
def add_player(username, roomnumber, turn, category, turn_fixed, date, rolled):
    return db.execute("INSERT INTO rooms (roomnumber, username, place, turn, category, turn_fixed, won, date, rolled) VALUES(:roomnumber, :username, :place, :turn, :category, :turn_fixed, :won, :date, :rolled)",
                username=username, roomnumber=roomnumber, place=1, turn=turn, category=category, turn_fixed=turn, won=-1, date=date, rolled=rolled)

# Define a function that deletes a player from a specific room
def delete_player(player, playerdata):
    return db.execute("DELETE FROM rooms WHERE username = :username AND roomnumber = :roomnumber",
                        username=player["username"], roomnumber=playerdata[0]["roomnumber"])

# Define a function that requests all data for a specific player
def player_data(user_id):
    return db.execute("SELECT username, date, turn, place, category, roomnumber, won, in_bridge, rolled FROM rooms WHERE user_id = :user_id",
                            user_id=session["user_id"])

# Define a function that requests the boarddata for a specific room
def board_data(roomnumber):
    return db.execute("SELECT username, place, turn, turn_fixed, date FROM rooms WHERE roomnumber = :roomnumber GROUP BY turn_fixed",
                            roomnumber=roomnumber)