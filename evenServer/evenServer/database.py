# -*- coding: utf-8 -*-
from evenServer import app
from flask import g
import sqlite3
from alarmObject import AlarmObject

TABLE_NAME = "alarms"
DESCRIPTION = "descrition"
HOUR = "hour"
MINUTE = "minute"
DAY = "day"


def connect():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def createEmptyDatabase():
    """Creates the database tables."""
    with app.app_context():
        db = getConnection()
        with app.open_resource('database_init.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def getConnection():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect()
    return g.sqlite_db

def execute(sql):
    db = getConnection()
    return db.execute(sql)

def insert(description, hour, minute, day):
    db = getConnection()
    db.execute("INSERT INTO " + TABLE_NAME + " VALUES (null, ?, ?, ?, ?)", [description, hour, minute, day])
    db.commit()

def delete(id):
    db = getConnection()
    db.execute("DELETE FROM " + TABLE_NAME + " WHERE _id=?", [description, hour, minute, day])
    db.commit()

def getAlarms():
    db = getConnection()
    cursor = db.execute("SELECT _id, description, hour, minute, day FROM alarms")
    rows = cursor.fetchall()
    alarmArray = [] 
    for row in rows:
        alarm = AlarmObject(row)
        alarmArray.append(alarm)
    return alarmArray

@app.teardown_appcontext
def closeConnection(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
