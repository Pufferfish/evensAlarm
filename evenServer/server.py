# -*- coding: utf-8 -*-
from evenServer import app
from evenServer import database as db

db.createEmptyDatabase()
app.run(debug=True, host="0.0.0.0")
