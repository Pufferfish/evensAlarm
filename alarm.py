#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import signal
import sys
from datetime import datetime
import sqlite3 as db

#################Globals###########################
blinketid = 0.003
loopsPerRotasjon = 500
blenders
buttonChange=0
pins = [7, 11, 13, 15]
alarms = []
OPPE = 0
NEDE = 1
#nighttime=true

#################Funksjoner###########################
def frontPersienneOppover(rotasjoner):
	print("--- Åpner persiennene ---")
	for i in range(0, rotasjoner * loopsPerRotasjon):
		for j in pins:
			setPinHigh(j)		
			time.sleep(blinketid)
	print("--- Persiennene åpne ---")

def frontPersienneNedover(rotasjoner):
	print("--- Lukker persiennene ---")
	for i in range(0, rotasjoner * loopsPerRotasjon):
		for j in reversed(pins):
			setPinHigh(j)		
			time.sleep(blinketid)
	print("--- Persiennene lukket ---")

def setPinHigh(pin):
		GPIO.output(7,   GPIO.LOW)	
		GPIO.output(11,  GPIO.LOW)
		GPIO.output(13,  GPIO.LOW)
		GPIO.output(15,  GPIO.LOW)
		GPIO.output(pin, GPIO.HIGH)

def wakeUpAt(hoursWU,minutesWU):
	global blenders
	if(hoursWU == int(klokken[0] + klokken[1]) and minutesWU == int(klokken[3] + klokken[4])):
		print("Alarm: Stå opp!")
		printTime()
		tryOpenBlinders()
	time.sleep(1)		

def closeBlendersAt(hoursCB,minutesCB):
	global blenders
	if(hoursCB==int(klokken[0]+klokken[1]) and minutesCB==int(klokken[3]+klokken[4])):
		print("Alarm: Leggetid!")
		printTime()
		tryCloseBlinders()
	time.sleep(1)			

def buttonToggleBlenders():
	global blenders
	global buttonChange
	if(buttonChange):
		if(GPIO.input(8) == 0):
			tryOpenBlinders()
		else:
			tryCloseBlinders()
	buttonChange = 0

def tryOpenBlinders():
	global blenders
	if(blenders == NEDE):
		frontPersienneOppover(7)
		blenders = OPPE

def tryCloseBlinders():
	global blenders
	if(blenders == OPPE):
		frontPersienneNedover(7)
		blenders = NEDE

def turnOffLights():
	GPIO.output(7,GPIO.LOW)	
	GPIO.output(11,GPIO.LOW)
	GPIO.output(13,GPIO.LOW)
	GPIO.output(15,GPIO.LOW)

def signal_handler(signal,frame):
	print("Program mottok SIG-INT")
	GPIO.cleanup()
	sys.exit(0)

def printTime():
		klokken = str(datetime.now().time())
		print("Kl: " + klokken)


##################MAIN#########################
def start():
	signal.signal(signal.SIGINT, signal_handler)
	global blender = GPIO.input(8)
	print("Starter vekkerklokken")
	printTime()

	while(1):
		
		helpvar = GPIO.input(8)
		time.sleep(4)
		#####################
		turnOffLights()
		time.sleep(4)
		#####################
		wakeUpAt(07,30)
		time.sleep(4)	
		#####################
		closeBlendersAt(22,30)
		time.sleep(4)
		#####################
		if(helpvar != GPIO.input(8)):
			buttonChange=1
		buttonToggleBlenders()
		#####################	

	GPIO.cleanup()

def main():
	initGPIO()
	# Fjern kommentering om det finnes en brukbar alarms.db
	#fetchAlarms()
	start()

def initGPIO():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)
	GPIO.setup(15, GPIO.OUT)
	GPIO.setup(26, GPIO.OUT)
	GPIO.setup(8, GPIO.IN)

def fetchAlarms():
	# http://docs.python.org/2/library/sqlite3.html
	connection = db.connect('alarms.db')
	cursor = connection.cursor()
	cursor.execute('SELECT hour, minute, day FROM alarms')
	# returnerer type (12, 50, MONDAY) elns
	rows = cursor.fetchall()
	for row in rows:
		alarms.append(row)
	connection.close()

if __name__ == "__main__":
	main()

	
