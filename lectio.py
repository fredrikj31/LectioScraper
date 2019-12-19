import re
import requests
from lxml import html
from bs4 import BeautifulSoup
from details import lectioUsername, lectioPassword


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
		authenticity_token = list(
			set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))[0]

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

	"""def login(self):
		LOGIN_URL = "https://www.lectio.dk/lectio/{}/login.aspx".format(self.SchoolId)

		# Start requests session and get eventvalidation key
		s = requests.Session()
		result = s.get(LOGIN_URL)
		# print(result.text)
		tree = html.fromstring(result.text)
		authenticity_token = list(
			set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))[0]

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
		result = s.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))

		return s"""

	def getExercises(self):
		EXERCISE_URL = "https://www.lectio.dk/lectio/680/OpgaverElev.aspx?elevid={}".format(self.studentId)

		# Scrape url
		result = self.Session.get(EXERCISE_URL)

		soup = BeautifulSoup(result.text, features="html.parser")

		table = soup.find("table", {"id": "s_m_Content_Content_ExerciseGV"})



		jsonText = {"Exercises": []}

		tableHeaders = table.findAll('th')

		exerciseList = {}

		Id = 0

		for row in table.findAll('td'):
			exerciseList.setdefault(tableHeaders[Id].text.replace("'", '"'), row.text)
			Id += 1

			if Id == 11:
				Id = 0
				jsonText['Exercises'].append(exerciseList)
				exerciseList = {}

		return jsonText


	def getSchedule(self): #Need some work!
		SCHEDULE_URL = "https://www.lectio.dk/lectio/680/SkemaNy.aspx?type=elev&elevid={}".format(self.studentId)

		result = self.Session.get(SCHEDULE_URL)

		soup = BeautifulSoup(result.text, features="html.parser")

		table = soup.find("table", {"id": "s_m_Content_Content_SkemaNyMedNavigation_skema_skematabel"})

		for row in soup.findAll('table')[0].tbody.findAll('tr'):
			first_column = row.findAll('th')[0].contents
			third_column = row.findAll('td')[2].contents
			print(first_column, third_column)

		


	#STILL NEED TO FIX THIS ONE!
	def getMessages(self):
		MESSAGE_URL = "https://www.lectio.dk/lectio/{}/beskeder2.aspx?type=&elevid={}&selectedfolderid=-70".format(self.SchoolId, self.studentId)

		result = self.Session.get(MESSAGE_URL)

		soup = BeautifulSoup(result.text, features="html.parser")

		table = soup.find("table", {"id": "s_m_Content_Content_threadGV"})

		jsonText = {"Messages": []}

		tableHeaders = table.findAll('th')

		messageList = {}

		Id = 0

		"""for row in table.findAll('td'):
			messageList.setdefault(tableHeaders[Id].text, row.text)
			Id += 1

			if Id == 11:
				Id = 0
				jsonText['Messages'].append(messageList)
				messageList = {}"""

		return tableHeaders