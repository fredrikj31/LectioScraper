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

		rows = []
		columns = []

		for row in table.findAll("tr"):
			#rows.append(row.contents)
			for row1 in row.findAll('td'):
				columns.append(row1.text)
			rows.append(columns)
			columns = []
		
		return rows