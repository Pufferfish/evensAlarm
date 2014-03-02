from evenServer import app
from alarmObject import AlarmObject
from flask import Flask, request, session, redirect, render_template
import database as db


@app.route("/")
def index():
	alarmArray = db.getAlarms()
	return render_template("layout.html", alarms=alarmArray)

@app.route("/add", methods=['POST'])
def addAlarm():
	description = request.form['description']
	time		= request.form['time']
	# Format: HH:MM
	minute		= time.split(':')[-1]
	hour 		= time.split(':')[0]
	day 		= request.form['day']
	db.insert(description, hour, minute, day)
	return redirect("/")

@app.route("/delete", methods=['POST'])
def deleteAlarm():
	id = request.form['id']
	db.delete(id)
	return redirect("/")

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == "POST":
	    if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
	        return render_template("login.html", error="Invalid username/password")

	    session['loggedIn'] = True
	    return redirect("/")
	else:
		return render_template("login.html", error=None)

@app.route('/logout')
def logout():
	loggedIn = session.get("loggedIn", False)
	if loggedIn:
		session.pop('loggedIn', None)
	return redirect("/")
