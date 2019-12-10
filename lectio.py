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

	def login(self):
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

		return s

	def getExercises(self):
		session = self.login()

		
