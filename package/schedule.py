import re
import requests
from lxml import html
from bs4 import BeautifulSoup

# FINISH OUTPUT
"""
[
	{
		"LessonId": "(Lesson Id)",
		"Status": "(Status)",
		"Title": "(Title)",
		"Time": "(Time)",
		"Team": "(Team)",
		"Teacher": "(Teacher)",
		"Room": "(Room)"
	},
	{
		...
	}
]

"""


def schedule(self, Session, SchoolId, StudentId):
	SCHEDULE_URL = "https://www.lectio.dk/lectio/{}/SkemaNy.aspx?type=elev&elevid={}".format(SchoolId, StudentId)

	result = Session.get(SCHEDULE_URL)

	soup = BeautifulSoup(result.text, features="html.parser")
	scheduleContainer = soup.findAll('a', {"class": "s2bgbox"})

	fullSchedule = []
	Schedule = {}


	for schedule in scheduleContainer:
		rows = schedule['data-additionalinfo'].split("\n")
		timeStructure = re.compile('\d{2}/\d+-\d{4} \d{2}:\d{2} til \d{2}:\d{2}')
		teamStructure = re.compile('Hold: ')
		teacherStructure = re.compile('Lærer.*: ')
		roomStructure = re.compile('Lokale.*: ')

		#Getting the lesson id
		# Get the lesson if normal
		if "absid" in schedule['href']:
			lessonIdSplit1 = schedule['href'].split("absid=")
		elif "ProeveholdId" in schedule['href']:
			lessonIdSplit1 = schedule['href'].split("ProeveholdId=")
		else:
			print("Error")
			return False
		
		lessonIdSplit2 = lessonIdSplit1[1].split("&prevurl=")
		lessonId = lessonIdSplit2[0]
		
		
		#Check if there is a status
		if rows[0] == "Aflyst!" or rows[0] == "Ændret!":
			#print("found a status: {}".format(rows[0]))

			status = rows[0]

			#Check if there is a title
			if timeStructure.match(rows[1]):
				#print("did not find a title")
				title = " "
			else:
				#print("found a title: {}".format(rows[1]))
				title = rows[1]

		else:
			#print("did not find any status")
			status = " "

			#Check if there is a title
			if timeStructure.match(rows[0]):
				#print("did not find a title")
				title = " "
			else:
				#print("found a title: {}".format(rows[0]))
				title = rows[0]

		time = list(filter(timeStructure.match, rows))
		team = list(filter(teamStructure.match, rows))
		teacher = list(filter(teacherStructure.match, rows))
		room = list(filter(roomStructure.match, rows))

		#If list is empty (There is no room or teacher) then make list empty
		if len(time) == 0:
			time = " "
		else:
			time = time[0]
		
		if len(team) == 0:
			team = " "
		else:
			team = team[0].split(":")[1].strip()
		
		if len(teacher) == 0:
			teacher = " "
		else:
			teacher = teacher[0].split(":")[1].strip()
		
		if len(room) == 0:
			room = " "
		else:
			room = room[0].split(":")[1].strip()

		#.split(":")[2]

		Schedule['Status'] = status
		Schedule['Title'] = title
		Schedule['Time'] = time
		Schedule['Team'] = team
		Schedule['Teacher'] = teacher
		Schedule['Room'] = room
		Schedule['Id'] = lessonId
		


		fullSchedule.append(Schedule)
		Schedule = {}

		
		#DEBUG PURPOSES
		"""
		print(time[0])
		print(team[0])
		print(teacher[0])
		print(room[0])
		
		print("---------------------------")"""

		
	return fullSchedule