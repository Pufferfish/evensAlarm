# -*- coding: utf-8 -*-

class AlarmObject:
	def __init__(self, sqlRow):
		self.id 		 = sqlRow[0]
		self.description = sqlRow[1]
		self.hour 		 = sqlRow[2]
		self.minute 	 = sqlRow[3]
		self.day  		 = sqlRow[4]

	def getDay(self):
		return {
			1: u'Mandag',
			2: u'Tirsdag',
			3: u'Onsdag',
			4: u'Torsdag',
			5: u'Fredag',
			6: u'Lørdag',
			7: u'Søndag'
		}[self.day]
