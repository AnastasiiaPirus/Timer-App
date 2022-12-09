from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

from datetime import datetime
import re

# Configure application


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

from index_get import render_index_get
from index_post import render_index_post

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords doesn't match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) == 1:
            return apology("username already exists", 400)

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        # Remember which user has logged in
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
        user_id = int(user_id[0]['user_id'])
        db.execute("INSERT INTO timers (user_id, is_paused, timeramount,  totaltime, timestamp ) VALUES(?,?, ? ,?, ?)",
                   user_id, True, 0, 0, "2011-11-11 11:11:11")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""
    user_id = session["user_id"]
    is_paused = db.execute("SELECT is_paused FROM timers WHERE user_id = ? ;", user_id)
    is_paused = is_paused[0]['is_paused']
    if is_paused == 0 :
    #pause user timer    
        is_paused = request.form.get("is_paused")
        upd_timestamp = datetime.now()
        old_timestamp = db.execute("SELECT timestamp FROM timers WHERE user_id = ? ;", user_id)
        old_timestamp = old_timestamp[0]['timestamp']
        old_timestamp = datetime.strptime(old_timestamp, '%Y-%m-%d %H:%M:%S')
        time_actual = (upd_timestamp - old_timestamp).seconds
        totaltime = db.execute("SELECT totaltime FROM timers WHERE user_id = ? ;", user_id)
        totaltime = totaltime[0]['totaltime']
        totaltime = totaltime + time_actual
        timeramount = db.execute("SELECT timeramount FROM timers WHERE user_id = ? ;", user_id)
        timeramount = int(timeramount[0]['timeramount'])
        timeramount = timeramount - time_actual
        db.execute("UPDATE timers SET timeramount = ?, is_paused = ?, totaltime = ? WHERE user_id = ? ;", 0,
                1, totaltime, user_id)
    # Forget any user_id
    session.clear()
    
    # Redirect user to login form
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    if request.method == "POST":
        return render_index_post(user_id)
    if request.method == "GET":
        return render_index_get(user_id)


@app.route("/field")
@login_required
def field():
    

    user_id = session["user_id"]
    timeramount = db.execute("SELECT timeramount FROM timers WHERE user_id= ?;", user_id)
    timeramount = int(timeramount[0]['timeramount'])
    username = db.execute("SELECT username FROM users WHERE user_id= ?;", user_id)
    username = username[0]['username']
    # print(username, "</h1>")
    timestamp = db.execute("SELECT timestamp FROM timers WHERE user_id= ?;", user_id)
    timestamp = timestamp[0]['timestamp']
    if timestamp  != '2011-11-11 11:11:11':
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        time_actual = (datetime.now() - timestamp).seconds
        # print(time_actual, "time_actual, normal")
    else:
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        time_actual = (timestamp - timestamp).seconds
        # print(time_actual, "time_actual, 11111")

    is_paused = db.execute("SELECT is_paused FROM timers WHERE user_id= ?;", user_id)
    is_paused = is_paused[0]['is_paused']
    # print(is_paused, "is_paused")
    if is_paused == 0:
        timeramount = timeramount - time_actual
    
    
    
    totaltime = db.execute("SELECT totaltime FROM timers WHERE user_id = ? ;", user_id)
    totaltime = totaltime[0]['totaltime']
    if is_paused == 0:
        totaltime = totaltime + time_actual
    # print(totaltime, "totaltime")

    # Location of next sprite
    next_sprite_location, seconds_to_unlock, sprite_id = render_next_monster_sprite(user_id, totaltime)

    # Calculations for progress bar
    progress_bar_actual, progress_bar_total = render_progress_bar(seconds_to_unlock, sprite_id, totaltime)

    list_of_locations = db.execute(
        "SELECT sprites.location FROM sprites JOIN backpack ON sprites.sprite_id = backpack.unlocked WHERE backpack.user_id = ? ;",
        user_id)


    if len(list_of_locations) > 0:
        locations = [d['location'] for d in list_of_locations]

        names = []
        for i in locations:
            name = (re.findall('static/imgs/sprites/(.*).png', i))
            name = ''.join(name)
            names.append(name)
        number_of_names = len(names)
        return render_template("field.html", timeramount=timeramount, is_paused=is_paused,
                           next_sprite_location=next_sprite_location, progress_bar_actual=progress_bar_actual,
                           progress_bar_total=progress_bar_total, username=username, number_of_names=number_of_names, names=names,)

    else: 
        return render_template("field.html", timeramount=timeramount, is_paused=is_paused,
                           next_sprite_location=next_sprite_location, progress_bar_actual=progress_bar_actual,
                           progress_bar_total=progress_bar_total, username=username)



    

def render_progress_bar(seconds_to_unlock, sprite_id, totaltime):
    if sprite_id > 1:
        seconds_for_previous = db.execute("SELECT seconds_to_unlock FROM sprites WHERE sprite_id = ? ;", (sprite_id - 1))
        seconds_for_previous = seconds_for_previous[0]['seconds_to_unlock']
    else:
        seconds_for_previous = 0
    # print(seconds_to_unlock, "seconds_to_unlock")
    # print(seconds_for_previous, "seconds_for_previous")
    # print(totaltime,"totaltime in render_progress_bar")
    progress_bar_total = seconds_to_unlock - seconds_for_previous
    progress_bar_actual = totaltime - seconds_for_previous
    # print(progress_bar_actual, "progress_bar_actual")
    return progress_bar_actual, progress_bar_total

def render_next_monster_sprite(user_id, totaltime):

    unlocked = db.execute("SELECT  unlocked FROM backpack   WHERE user_id = ? ORDER BY unlocked DESC LIMIT 1;", user_id)
    # print(unlocked)
    if len(unlocked) > 0:

        unlocked = int(unlocked[0]['unlocked'])
        sprite_id = unlocked + 1
        # print("one already unlocked", sprite_id)
    else:
        sprite_id = 1
    next_sprite_location = db.execute("SELECT location FROM sprites WHERE sprite_id = ? ;", sprite_id)
    
    if len(next_sprite_location) > 0:
        next_sprite_location = next_sprite_location[0]['location']

        seconds_to_unlock = db.execute("SELECT seconds_to_unlock FROM sprites WHERE sprite_id = ? ;", sprite_id)
        seconds_to_unlock = seconds_to_unlock[0]['seconds_to_unlock']

        
        # print(seconds_to_unlock, "seconds_to_unlock in render_next_monster_sprite")
        if totaltime >= seconds_to_unlock:
            db.execute("INSERT INTO backpack (unlocked, user_id) VALUES(?, ?)", sprite_id, user_id)
            sprite_id = sprite_id + 1
    else:
        seconds_to_unlock = 100000
        # totaltime = db.execute("SELECT totaltime FROM timers WHERE user_id = ? ;", user_id)
        # totaltime = totaltime[0]['totaltime']

    next_sprite_location = db.execute("SELECT location FROM sprites WHERE sprite_id = ? ;", sprite_id)
    next_sprite_location = next_sprite_location[0]['location']
    seconds_to_unlock = db.execute("SELECT seconds_to_unlock FROM sprites WHERE sprite_id = ? ;", sprite_id)
    seconds_to_unlock = seconds_to_unlock[0]['seconds_to_unlock']
    # totaltime = db.execute("SELECT totaltime FROM timers WHERE user_id = ? ;", user_id)
    # totaltime = totaltime[0]['totaltime']

    return next_sprite_location, seconds_to_unlock, sprite_id