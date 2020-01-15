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


	#Get school id's
	def getSchools(self):
		SCHOOLS_URL = "https://www.lectio.dk/lectio/login_list.aspx"

		result = requests.get(SCHOOLS_URL)

		SchoolsList = {}

		soup = BeautifulSoup(result.text, features="html.parser")
		schools = soup.findAll("a", href=True)
		for school in schools:
			schoolId = school['href'].split('/')
			if len(schoolId) == 4:
				SchoolsList[school.getText()] = schoolId[2]
			else:
				continue

		return SchoolsList



	def getExercises(self):
		EXERCISE_URL = "https://www.lectio.dk/lectio/680/OpgaverElev.aspx?elevid={}".format(self.studentId)

		# Scrape url
		result = self.Session.get(EXERCISE_URL)
		
		soup = BeautifulSoup(result.text, features="html.parser")
		table = soup.find("table", {"id": "s_m_Content_Content_ExerciseGV"})
		Exercises = []
		tableHeaders = table.findAll('th')
		exerciseList = {}

		Id = 0
		for row in table.findAll('td'):
			exerciseList.setdefault(tableHeaders[Id].text.replace("'", '"'), row.text)
			Id += 1
			if Id == 11:
				Id = 0
				Exercises.append(exerciseList)
				exerciseList = {}

		return Exercises


	#Need some work!
	def getSchedule(self):
		SCHEDULE_URL = "https://www.lectio.dk/lectio/680/SkemaNy.aspx?type=elev&elevid={}".format(self.studentId)

		result = self.Session.get(SCHEDULE_URL)

		soup = BeautifulSoup(result.text, features="html.parser")
		scheduleContainer = soup.findAll('div', {"class": "s2skemabrikcontainer"})

		for schedule in scheduleContainer:
			for time in schedule.findAll('a', {"class": "s2skemabrik"}):
				print(" ")
				print(" ")
				row = time['data-additionalinfo'].split("\n")
				print(row)
				#17/1-2020 13:20 til 14:20'
				if re.match('\d{2}/\d+-\d{4} \d{2}:\d{2} til \d{2}:\d{2}', row[0]):
					print("WE FOUND A TIMESTAMP")
					time = row[0]
				elif re.match('\d{2}/\d+-\d{4} \d{2}:\d{2} til \d{2}:\d{2}', row[1]):
					print("WE FOUND A TIMESTAMP")
					time = row[1]
				print(" ")
				print(" ")


	def getMessages(self):
		MESSAGE_URL = "https://www.lectio.dk/lectio/{}/beskeder2.aspx?type=&elevid={}&selectedfolderid=-70".format(self.SchoolId, self.studentId)

		result = self.Session.get(MESSAGE_URL)

		soup = BeautifulSoup(result.text, features="html.parser")

		table = soup.find("table", {"id": "s_m_Content_Content_threadGV"})

		Id = 0
		Messages = []
		Message = {}

		Informations = []

		for row in table.findAll('tr'):
			if Id == 0:
				Id += 1
				continue
			else:
				#print("THIS IS A TEST")
				for column in row:
					Informations.append(column)

				Message['Title'] = Informations[4].getText().strip()
				Message['Last Message'] = Informations[5].getText().strip()
				Message['First Message'] = Informations[6].getText().strip()
				for elem in Informations[7]:
					recipients = elem['title'].strip()
				Message['Recipients'] = recipients
				Message['Last Update'] = Informations[8].getText().strip()
					
				Messages.append(Message)
				Informations = []
				Message = {}
			

		return Messages