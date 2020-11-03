import re
import requests
from lxml import html
from bs4 import BeautifulSoup

def studyProgramme(self, Session, SchoolId, StudentId):
	STUDIERETNING_URL = "https://www.lectio.dk/lectio/{}/studieretningElevValg.aspx?elevid={}".format(SchoolId, StudentId)

	result = Session.get(STUDIERETNING_URL)

	output = {}

	soup = BeautifulSoup(result.text, features="html.parser")
	table = soup.find('div', {'class': "islandContent"})
	
	rows = table.findAll('tr')

	output['Elev Type'] = rows[0].find('td').getText().strip()
	output['Elev Start'] = rows[1].find('td').getText().strip()
	output['Studieretning'] = rows[2].find('td').getText().strip()

	return output