import re
import requests
from lxml import html
from bs4 import BeautifulSoup
from details import lectioUsername, lectioPassword


#Packages
from package import exercises, exercise, message, messages, schedule, schools, studyProgramme, unreadMessages


class Lectio:

	def __init__(self, Username, Password, SchoolId):
		self.Username = Username
		self.Password = Password
		self.SchoolId = SchoolId

		LOGIN_URL = "https://www.lectio.dk/lectio/{}/login.aspx".format(self.SchoolId)

		# Start requests session and get eventvalidation key
		session = requests.Session()
		result = session.get(LOGIN_URL)
		# print(result.text)
		tree = html.fromstring(result.text)
		authenticity_token = list(set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))[0]

		# Create payload
		payload = {
			"m$Content$username2": self.Username,
			"m$Content$password2": self.Password,
			"m$Content$passwordHidden": self.Password,
			"__EVENTVALIDATION": authenticity_token,
			"__EVENTTARGET": "m$Content$submitbtn2",
			"__EVENTARGUMENT": "",
			"LectioPostbackId": ""
		}

		# Perform login
		result = session.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))

		# Getting student id
		dashboard = session.get("https://www.lectio.dk/lectio/680/forside.aspx")
		soup = BeautifulSoup(dashboard.text, features="html.parser")
		studentIdFind = soup.find("a", {"id": "s_m_HeaderContent_subnavigator_ctl01"}, href=True)

		self.studentId = (studentIdFind['href']).replace("/lectio/680/forside.aspx?elevid=", '')

		self.Session = session

	def getSchools(self):
		result = schools.schools(self)

		return result

	def getExercise(self, ExerciseId):
		result = exercise.exercise(self, self.Session, self.SchoolId, self.studentId, ExerciseId)

		return result
	
	def getExercises(self):
		result = exercises.exercises(self, self.Session, self.SchoolId, self.studentId)

		return result
	
	def getMessages(self):
		result = messages.messages(self, self.Session, self.SchoolId, self.studentId)

		return result
	
	def getMessage(self, MessageId):
		result = message.message(self, self.Session, self.SchoolId, self.studentId, MessageId)

		return result
	
	def getSchedule(self):
		result = schedule.schedule(self, self.Session, self.SchoolId, self.studentId)

		return result

	def getStudyProgramme(self):
		result = studyProgramme.studyProgramme(self, self.Session, self.SchoolId, self.studentId)

		return result

	def getUnreadMessages(self):
		result = unreadMessages.unreadMessages(self, self.Session, self.SchoolId)

		return result