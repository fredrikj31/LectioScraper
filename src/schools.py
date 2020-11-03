import re
import requests
from lxml import html
from bs4 import BeautifulSoup

def schools(self):
	SCHOOLS_URL = "https://www.lectio.dk/lectio/login_list.aspx"

	result = requests.get(SCHOOLS_URL)

	SchoolsList = []
	School = {}

	soup = BeautifulSoup(result.text, features="html.parser")
	schools = soup.findAll("a", href=True)
	for school in schools:
		schoolId = school['href'].split('/')


		if len(schoolId) == 4:
			School['Navn'] = school.getText()
			School['Nummer'] = schoolId[2]

			SchoolsList.append(School)
			School = {}
		else:
			continue

	return SchoolsList