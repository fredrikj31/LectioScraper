import re
import requests
from lxml import html
from bs4 import BeautifulSoup

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