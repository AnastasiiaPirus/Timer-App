from datetime import datetime

from flask import request, redirect

from app import db


def render_index_post(user_id):
    if "minutes" in request.form:
        return start_timer(user_id)

    elif "is_paused" in request.form:
        return pause_timer(user_id)

    elif "resume" in request.form:
        return resume_timer(user_id)

    elif "stop" in request.form:
        return stop_timer(user_id)

    elif "finished" in request.json:
        return finish_timer(user_id)
    
    else :
        # print ("upgrade")
        return upgrade(user_id)
    
    


def start_timer(user_id):
    minutes = request.form.get("minutes")
    seconds = int(minutes)  # *60
    db.execute("UPDATE timers SET timeramount = ? WHERE user_id= ? ;", seconds, user_id)
    timestamp = datetime.now()
    db.execute("UPDATE timers SET timestamp = ? WHERE user_id= ? ;", timestamp.strftime('%Y-%m-%d %H:%M:%S'),
               user_id)
    db.execute("UPDATE timers SET is_paused = ? WHERE user_id= ? ;", 0, user_id)
    return redirect("/")


def finish_timer(user_id):
    finished = request.json.get("finished")
    
    timeramount = db.execute("SELECT timeramount FROM timers WHERE user_id = ? ;", user_id)
    timeramount = int(timeramount[0]['timeramount'])
    totaltime = db.execute("SELECT totaltime FROM timers WHERE user_id = ? ;", user_id)
    totaltime = totaltime[0]['totaltime']
    totaltime = int(totaltime) + timeramount
    # print(finished, "finished")
    db.execute("UPDATE timers SET timeramount = ?, is_paused = ?, totaltime = ? WHERE user_id = ? ;", 0, finished,
               totaltime, user_id)
    return redirect("/")


def stop_timer(user_id):
    # print("stop clicked")
    timeramount = db.execute("SELECT timeramount FROM timers WHERE user_id = ? ;", user_id)
    timeramount = int(timeramount[0]['timeramount'])
    upd_timestamp = datetime.now()
    old_timestamp = db.execute("SELECT timestamp FROM timers WHERE user_id = ? ;", user_id)
    old_timestamp = old_timestamp[0]['timestamp']
    old_timestamp = datetime.strptime(old_timestamp, '%Y-%m-%d %H:%M:%S')
    time_actual = (upd_timestamp - old_timestamp).seconds
    # print(time_actual, "time_actual")
    timeramount = time_actual
    totaltime = db.execute("SELECT totaltime FROM timers WHERE user_id = ? ;", user_id)
    totaltime = totaltime[0]['totaltime']
    # print(totaltime, "totaltime")
    is_paused = db.execute("SELECT is_paused FROM timers WHERE user_id = ? ;", user_id)
    is_paused = int(is_paused[0]['is_paused'])
    if is_paused == 0:
        totaltime = int(totaltime) + timeramount
    db.execute("UPDATE timers SET timeramount = ?, is_paused = ?, totaltime = ? WHERE user_id = ? ;", 0, 1,
               totaltime, user_id)
    return redirect("/")


def resume_timer(user_id):
    timeramount = db.execute("SELECT timeramount FROM timers WHERE user_id = ? ;", user_id)
    timeramount = int(timeramount[0]['timeramount'])
    minutes = timeramount
    seconds = int(minutes)  # *60
    # db.execute("UPDATE timers SET timeramount = ? WHERE user_id= ? ;", seconds , user_id)
    timestamp = datetime.now()
    
    db.execute("UPDATE timers SET is_paused = ?, timestamp = ?, timeramount = ? WHERE user_id= ? ;", 0,
               timestamp.strftime('%Y-%m-%d %H:%M:%S'), seconds, user_id)
    # db.execute("UPDATE timers SET is_paused = ? WHERE user_id= ? ;", 0 , user_id)
    is_paused = 0
    # return render_template("index.html", timeramount=timeramount, is_paused=is_paused)
    return redirect("/")


def pause_timer(user_id):
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
    db.execute("UPDATE timers SET timeramount = ?, is_paused = ?, totaltime = ? WHERE user_id = ? ;", timeramount,
               1, totaltime, user_id)
    # return render_template("index.html", timeramount=timeramount, is_paused=is_paused)
    return redirect("/")

def upgrade(user_id):
    # print(1)
    upd_timestamp = datetime.now()
    # print(2)
    old_timestamp = db.execute("SELECT timestamp FROM timers WHERE user_id = ? ;", user_id)
    old_timestamp = old_timestamp[0]['timestamp']
    old_timestamp = datetime.strptime(old_timestamp, '%Y-%m-%d %H:%M:%S')
    time_actual = (upd_timestamp - old_timestamp).seconds
    # print(3)
    totaltime = db.execute("SELECT totaltime FROM timers WHERE user_id = ? ;", user_id)
    # totaltime = totaltime[0]['totaltime']
    # totaltime = totaltime + time_actual
    # print(4)
    timeramount = db.execute("SELECT timeramount FROM timers WHERE user_id = ? ;", user_id)
    timeramount = int(timeramount[0]['timeramount'])
    timeramount = timeramount - time_actual
    # print(5)
    
    db.execute("UPDATE timers SET timeramount = ?, totaltime = ?, timestamp = ? WHERE user_id = ? ;", timeramount,  totaltime, upd_timestamp, user_id)

    # timeramount = db.execute("SELECT timeramount FROM timers WHERE user_id = ? ;", user_id)
    # timeramount = int(timeramount[0]['timeramount'])
    # minutes = timeramount
    # seconds = int(minutes)  # *60

    # db.execute("UPDATE timers SET timeramount = ? WHERE user_id= ? ;", seconds , user_id)
    # timestamp = datetime.now()
    # print(6)
    # db.execute("UPDATE timers SET  timestamp = ? WHERE user_id= ? ;", timestamp.strftime('%Y-%m-%d %H:%M:%S'), user_id)
    # print(7)
    return redirect("/")
