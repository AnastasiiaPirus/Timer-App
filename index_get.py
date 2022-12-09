from datetime import datetime

from flask import render_template

from app import db


def render_index_get(user_id):
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

    return render_template("index.html", timeramount=timeramount, is_paused=is_paused,
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