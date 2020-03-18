import re
import requests
from lxml import html
from bs4 import BeautifulSoup

"""#Title exists
Schedule["LessonId"] = lessonId
Schedule["Status"] = row[0]
Schedule["Title"] = row[1]
Schedule["Date"] = row[2]
Schedule["Team"] = row[3]
Schedule["Teacher"] = row[3]
Schedule["Room"] = row[4]"""

# FINISH OUTPUT
"""

[
	{
		"LessonId": "(Lesson Id)",
		"Status": "(Status)",
		"Title": "(Title)",
		"Team": "(Team)",
		"Teacher": "(Teacher)",
		"Room": "(Room)"
	}
]


"""


def getSchedule(self, Session, StudentId):
	SCHEDULE_URL = "https://www.lectio.dk/lectio/680/SkemaNy.aspx?type=elev&elevid={}".format(StudentId)

	result = Session.get(SCHEDULE_URL)

	soup = BeautifulSoup(result.text, features="html.parser")
	scheduleContainer = soup.findAll('a', {"class": "s2bgbox"})

	fullSchedule = []
	Schedule = {}


	for schedule in scheduleContainer:
		n = 0
		rows = schedule['data-additionalinfo'].split("\n")
		timeStructure = re.compile('\d{2}/\d+-\d{4} \d{2}:\d{2} til \d{2}:\d{2}')
		teamStructure = re.compile('Hold: ')
		teacherStructure = re.compile('Lærer.*: ')
		roomStructure = re.compile('Lokale: ')
		time = list(filter(timeStructure.match, rows))
		team = list(filter(teamStructure.match, rows))
		teacher = list(filter(teacherStructure.match, rows))
		room = list(filter(roomStructure.match, rows))
		print(time)
		print(team)
		print(teacher)
		print(room)
		print("---------------------------")

		
	return fullSchedule