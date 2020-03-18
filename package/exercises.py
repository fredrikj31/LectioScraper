import re
import requests
from lxml import html
from bs4 import BeautifulSoup

def Exercises(self, Session):
	EXERCISE_URL = "https://www.lectio.dk/lectio/680/OpgaverElev.aspx?elevid={}".format(self.studentId)

	# Scrape url
	result = Session.get(EXERCISE_URL)
		
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