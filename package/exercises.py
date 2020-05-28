import re
import requests
from lxml import html
from bs4 import BeautifulSoup

def exercises(self, Session, SchoolId, StudentId):
	EXERCISE_URL = "https://www.lectio.dk/lectio/{}/OpgaverElev.aspx?elevid={}".format(SchoolId, StudentId)

	# Scrape url
	result = Session.get(EXERCISE_URL)
		
	soup = BeautifulSoup(result.text, features="html.parser")
	table = soup.find("table", {"id": "s_m_Content_Content_ExerciseGV"})
	Exercises = []
	tableHeaders = table.findAll('th')
	exerciseList = {}

	Id = 0
	for row in table.findAll('td'):
		findExerciseId = row.findAll('a')
		
		if len(findExerciseId):
			exerciseIdSplit1 = str(findExerciseId[0])
			exerciseIdSplit2 = exerciseIdSplit1.split("&")[1]
			exerciseId = exerciseIdSplit2.split("exerciseid=")[1]


			#print(exerciseId)
			exerciseList['Id'] = exerciseId

		exerciseList.setdefault(tableHeaders[Id].text.replace("'", '"'), row.text)
		Id += 1
		if Id == 11:
			Id = 0
			Exercises.append(exerciseList)
			exerciseList = {}

	return Exercises